Get-SpeechToken -Region southcentralus -Key "7ee718737f6e4662b638d0b1f2342132"
#SpeechVoicesList | Where-Object -Property Shortname -Contains 'en'| Format-Table
#$files = Get-ChildItem -Path "D:\TMH\Code\Automated_Youtube\Output\" -Include *.txt | where name -Like "*new*"
$files = Get-ChildItem -Path "D:\TMH\Code\Automated_Youtube\Output\*.txt" -Recurse
$filename = $null

foreach ($file in $files)
{
    $filename = $file.Name
    $filename = $filename.Substring(0, $filename.LastIndexOf('.'))
    $text = Get-Content $file -raw

    Convert-TextToSpeech -Voice en-GB-RyanNeural -Text $text -Path "D:\TMH\Code\Automated_Youtube\Audio\$filename.mp3"
    Move-Item -Path $file -Destination "D:\TMH\Code\Automated_Youtube\UsedText"
}


