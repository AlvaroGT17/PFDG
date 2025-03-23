// frontend/main.cjs
const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let backendProcess;

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
        },
    });

    // ✅ Limpiar la caché ANTES de cargar el frontend
    win.webContents.session.clearCache().then(() => {
        console.log('✅ Caché de Electron limpia');

        // ✅ Cargar SOLO el archivo index.html (HashRouter se encargará del login)
        win.loadFile(path.join(__dirname, 'dist', 'index.html'));
    });
}

app.whenReady().then(() => {
    // ✅ Iniciar el backend al arrancar Electron
    backendProcess = spawn('node', ['../backend/index.js'], {
        cwd: path.join(__dirname, '..', 'backend'),
        shell: true,
    });

    backendProcess.stdout.on('data', (data) => {
        console.log(`Backend: ${data}`);
    });

    backendProcess.stderr.on('data', (data) => {
        console.error(`Backend error: ${data}`);
    });

    createWindow();

    // ✅ Cierre seguro del backend cuando la app se cierra
    app.on('before-quit', () => {
        if (backendProcess) {
            console.log('🛑 Cerrando backend desde before-quit...');
            backendProcess.kill();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit(); // Esto disparará el before-quit
    }
});
