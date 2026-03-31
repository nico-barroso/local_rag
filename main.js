const { app, BrowserWindow } = require("electron");

function waitForStreamlit() {
  return new Promise((resolve) => {
    const interval = setInterval(async () => {
      try {
        await fetch("http://localhost:8501");
        clearInterval(interval);
        resolve();
      } catch {
        // todavía no está listo, seguimos esperando
      }
    }, 1000);
  });
}

const createWindow = async () => {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
  });

  await waitForStreamlit();
  win.loadURL("http://localhost:8501");
};

app.whenReady().then(() => {
  createWindow();
});
