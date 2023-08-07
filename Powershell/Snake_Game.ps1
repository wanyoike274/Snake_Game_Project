function New-Game {
    $width = 20
    $height = 10
    $snake = @((5, 5))
    $food = New-Food
    $direction = "right"
    $score = 0
    $gameOver = $false

    while (-not $gameOver) {
        Draw-Game
        Move-Snake
        if (Check-Collision) {
            $gameOver = $true
        }
        if ($snake[0] -eq $food) {
            $snake += $snake[-1]
            $food = New-Food
            $score++
        }
        Start-Sleep -Milliseconds 200
    }

    Write-Host "Game Over! Your score: $score"
}

function Draw-Game {
    Clear-Host
    $board = @()
    for ($y = 0; $y -lt $height; $y++) {
        $row = 0..($width-1) | ForEach-Object { ' ' }
        $board += $row
    }
    foreach ($segment in $snake) {
        $board[$segment[1]][$segment[0]] = "O"
    }
    $board[$food[1]][$food[0]] = "*"

    $board | ForEach-Object { $_ -join "" }
}

function Move-Snake {
    $head = $snake[0]
    switch ($direction) {
        "up" { $newHead = ($head[0], $head[1] - 1) }
        "down" { $newHead = ($head[0], $head[1] + 1) }
        "left" { $newHead = ($head[0] - 1, $head[1]) }
        "right" { $newHead = ($head[0] + 1, $head[1]) }
    }
    $snake = $newHead, $snake[0..($snake.Length - 2)]
}

function Check-Collision {
    $head = $snake[0]
    if ($head[0] -lt 0 -or $head[0] -ge $width -or $head[1] -lt 0 -or $head[1] -ge $height) {
        return $true
    }
    $snake | Select-Object -Skip 1 | ForEach-Object {
        if ($_ -eq $head) {
            return $true
        }
    }
    return $false
}

function New-Food {
    $x = Get-Random -Minimum 0 -Maximum $width
    $y = Get-Random -Minimum 0 -Maximum $height
    return $x, $y
}

function Read-Direction {
    while ($true) {
        $key = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown").Character
        if ($key -eq "w" -or $key -eq "W") { return "up" }
        if ($key -eq "s" -or $key -eq "S") { return "down" }
        if ($key -eq "a" -or $key -eq "A") { return "left" }
        if ($key -eq "d" -or $key -eq "D") { return "right" }
    }
}

# Main game loop
function Start-SnakeGame {
    $global:direction = "right"

    $gameLoop = {
        param ($key)
        $global:direction = $key
    }

    $keyListener = $Host.UI.RawUI.ReadKeyAsync($gameLoop)

    New-Game
}

Start-SnakeGame
