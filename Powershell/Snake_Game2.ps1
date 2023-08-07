Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$Width = 20
$Height = 20
$TileSize = 20
$Snake = New-Object Collections.Generic.List[System.Drawing.Point]
$Food = [System.Drawing.Point]::Empty
$Direction = "Right"
$Score = 0
$GameOver = $false

function Draw-Game {
    $Graphics.Clear([System.Drawing.Color]::Black)

    foreach ($point in $Snake) {
        $Graphics.FillRectangle([System.Drawing.Brushes]::Green, $point.X * $TileSize, $point.Y * $TileSize, $TileSize, $TileSize)
    }

    $Graphics.FillRectangle([System.Drawing.Brushes]::Red, $Food.X * $TileSize, $Food.Y * $TileSize, $TileSize, $TileSize)

    $Graphics.DrawString("Score: $Score", [System.Drawing.Font]::Default, [System.Drawing.Brushes]::White, 5, $Height * $TileSize + 5)

    $PictureBox.Refresh()
}

function Move-Snake {
    $head = $Snake[0]
    $newHead = New-Object System.Drawing.Point($head.X, $head.Y)

    switch ($Direction) {
        "Up"    { $newHead.Y-- }
        "Down"  { $newHead.Y++ }
        "Left"  { $newHead.X-- }
        "Right" { $newHead.X++ }
    }

    if ($newHead.X -lt 0 -or $newHead.X -ge $Width -or $newHead.Y -lt 0 -or $newHead.Y -ge $Height -or $Snake.Contains($newHead)) {
        $GameOver = $true
    } else {
        $Snake.Insert(0, $newHead)

        if ($newHead -eq $Food) {
            $Score++
            $Food = Get-RandomPosition
        } else {
            $Snake.RemoveAt($Snake.Count - 1)
        }
    }
}

function Get-RandomPosition {
    $x = Get-Random -Minimum 0 -Maximum $Width
    $y = Get-Random -Minimum 0 -Maximum $Height
    return New-Object System.Drawing.Point($x, $y)
}

function On-TimerTick {
    Move-Snake
    Draw-Game

    if ($GameOver) {
        $Timer.Stop()
        [System.Windows.Forms.MessageBox]::Show("Game Over! Your score: $Score")
        $Form.Close()
    }
}

$Form = New-Object System.Windows.Forms.Form
$Form.Text = "Snake Game"
$Form.Size = New-Object System.Drawing.Size($Width * $TileSize, ($Height + 1) * $TileSize)
$Form.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::FixedSingle
$Form.StartPosition = [System.Windows.Forms.FormStartPosition]::CenterScreen

$PictureBox = New-Object System.Windows.Forms.PictureBox
$PictureBox.Size = $Form.Size
$PictureBox.BackColor = [System.Drawing.Color]::Black
$PictureBox.TabStop = $false
$Form.Controls.Add($PictureBox)

$Graphics = $PictureBox.CreateGraphics()

$Timer = New-Object System.Windows.Forms.Timer
$Timer.Interval = 200
$Timer.Add_Tick({ On-TimerTick })
$Timer.Start()

$Snake.Add([System.Drawing.Point]::Empty)
$Food = Get-RandomPosition

$Form.ShowDialog()
