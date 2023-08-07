// Snake Game JavaScript Code
document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('gameCanvas');
  const ctx = canvas.getContext('2d');
  const box = 20;
  const canvasSize = canvas.width / box;

  // Snake initial position
  let snake = [
    { x: canvasSize / 2, y: canvasSize / 2 }
  ];

  // Food initial position
  let food = { x: Math.floor(Math.random() * canvasSize), y: Math.floor(Math.random() * canvasSize) };

  // Initial direction
  let direction = 'right';

  // Function to draw a box on the canvas
  function drawBox(x, y, color) {
    ctx.fillStyle = color;
    ctx.fillRect(x * box, y * box, box, box);
    ctx.strokeStyle = 'black';
    ctx.strokeRect(x * box, y * box, box, box);
  }

  // Function to draw the entire game
  function drawGame() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the snake
    for (let i = 0; i < snake.length; i++) {
      drawBox(snake[i].x, snake[i].y, i === 0 ? 'green' : 'lightgreen');
    }

    // Draw the food
    drawBox(food.x, food.y, 'red');
  }

  // Function to update the game state
  function update() {
    // Move the snake
    const head = { ...snake[0] };
    switch (direction) {
      case 'up':
        head.y--;
        break;
      case 'down':
        head.y++;
        break;
      case 'left':
        head.x--;
        break;
      case 'right':
        head.x++;
        break;
    }

    // Check if the snake eats the food
    if (head.x === food.x && head.y === food.y) {
      snake.unshift(head);
      food = { x: Math.floor(Math.random() * canvasSize), y: Math.floor(Math.random() * canvasSize) };
    } else {
      snake.pop();
      snake.unshift(head);
    }

    // Check for game over conditions
    if (
      head.x < 0 || head.x >= canvasSize ||
      head.y < 0 || head.y >= canvasSize ||
      snake.some((segment, index) => index !== 0 && segment.x === head.x && segment.y === head.y)
    ) {
      clearInterval(gameInterval);
      alert('Game Over! Your score: ' + (snake.length - 1));
      location.reload();
    }

    // Redraw the game
    drawGame();
  }

  // Handle keyboard input for changing direction
  document.addEventListener('keydown', (event) => {
    switch (event.key) {
      case 'ArrowUp':
        direction = 'up';
        break;
      case 'ArrowDown':
        direction = 'down';
        break;
      case 'ArrowLeft':
        direction = 'left';
        break;
      case 'ArrowRight':
        direction = 'right';
        break;
    }
  });

  // Start the game loop
  const gameInterval = setInterval(update, 200);
});
