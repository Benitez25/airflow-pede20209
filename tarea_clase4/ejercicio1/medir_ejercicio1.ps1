# Ejecutar desde la carpeta donde se encuentra docker-compose.yaml.

$dagId = "reportes_ciudades_concurrencia"
$runId = "medicion_" + (Get-Date -Format "yyyyMMdd_HHmmss")

$elapsed = Measure-Command {
    docker compose exec -T airflow-scheduler airflow dags trigger $dagId -r $runId | Out-Host

    do {
        Start-Sleep -Seconds 2
        $json = docker compose exec -T airflow-scheduler airflow dags list-runs -d $dagId -o json
        $runs = $json | ConvertFrom-Json
        $run = $runs | Where-Object { $_.run_id -eq $runId } | Select-Object -First 1

        if ($null -eq $run) {
            $state = "not_found_yet"
        } else {
            $state = $run.state
        }

        Write-Host "Run: $runId | Estado: $state"
    }
    while ($state -notin @("success", "failed"))
}

Write-Host "Tiempo total: $([math]::Round($elapsed.TotalSeconds, 2)) segundos"
