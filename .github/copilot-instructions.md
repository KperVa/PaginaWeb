# Instrucciones del proyecto


## Arquitectura


- Es una página estática hecha con HTML, CSS y JavaScript nativos. No añadas frameworks, dependencias, herramientas de compilación ni gestores de paquetes sin que el proyecto lo requiera.
- `index.html` contiene la estructura, `styles.css` los estilos y `script.js` el comportamiento. Mantén cada responsabilidad en su archivo.
- El proyecto se puede abrir directamente en el navegador; también se puede servir con `python -m http.server 8000`. No presupongas que existen comandos de build, lint o test.


## Convenciones


- Mantén el contenido en español y usa HTML semántico, atributos accesibles y controles nativos.
- Conserva el diseño adaptable y respeta `prefers-reduced-motion` al añadir animaciones o transiciones.
- Si cambias identificadores o clases usados por JavaScript, actualiza también sus referencias en los otros archivos.
- Conserva el script con `defer` para que el HTML se analice antes de ejecutar el JavaScript.
- Usa el rojo para los elementos que deban ser llamativos en la web.


## Validación


- Para cambios de interfaz o comportamiento, comprueba la página en un navegador y verifica los tamaños de pantalla y estados interactivos afectados.
- Para cambios que solo afecten a un archivo, revisa que HTML, CSS y JavaScript sigan conectados correctamente. No añadas infraestructura de pruebas para cambios pequeños.