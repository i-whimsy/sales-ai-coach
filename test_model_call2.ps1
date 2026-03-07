$jsonData = @{
    task_name = "语音转写"
    input_data = @{
        file_path = "test.wav"
    }
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://localhost:8001/api/v1/models/call' `
                                 -Method POST `
                                 -Body $jsonData `
                                 -ContentType 'application/json' `
                                 -ErrorAction Stop
    Write-Host "✅ Request successful"
    Write-Host "Model ID: $($response.model_id)"
    Write-Host "Model Name: $($response.model_name)"
    Write-Host "Success: $($response.success)"
    Write-Host "Result:" $response.result
}
catch {
    Write-Host "❌ Request failed"
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode
        $statusDesc = $_.Exception.Response.StatusDescription
        
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseText = $reader.ReadToEnd()
        
        Write-Host "Status Code: $statusCode"
        Write-Host "Status Description: $statusDesc"
        Write-Host "Response Content:"
        $responseText
    }
    else {
        Write-Host "Error: $($_.Exception.Message)"
    }
}