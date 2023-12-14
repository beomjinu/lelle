const {app, BrowserWindow} = require("electron");

const createWindow = () => {
    const win = new BrowserWindow({
        width: 600,
        height: 550,
        titleBarStyle: "hiddenInset",
    });
    
    win.loadURL("http://localhost:5173/workspace/");
}

app.whenReady().then(() => {
    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    })
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});
