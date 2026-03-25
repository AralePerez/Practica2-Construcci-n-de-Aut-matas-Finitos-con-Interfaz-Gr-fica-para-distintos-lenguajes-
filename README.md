# Práctica de Autómatas – Lista 2 (AFN)

## Introducción

Este repositorio contiene el desarrollo de la práctica de autómatas enfocado en la **Lista 2**, donde originalmente se trabajó con **AFD (Autómatas Finitos Deterministas)** y posteriormente se realizó su conversión a **AFN (Autómatas Finitos No Deterministas)**.

Además, se incluye una aplicación con interfaz gráfica que permite trabajar con los autómatas desarrollados.

---

## Objetivo

El objetivo de esta práctica es:

* Diseñar autómatas utilizando JFLAP
* Comprender la conversión entre distintos tipos de autómatas
* Implementar una aplicación que permita trabajar con estos modelos
* Validar cadenas de entrada utilizando los autómatas construidos

---

## Contenido del repositorio

### Lista 2 – Autómatas

Se incluyen los autómatas correspondientes a la Lista 2:

* Autómatas diseñados en JFLAP (`.jff`)
* Versiones exportadas en:

  * `.json`
  * `.xml`
* Conversión realizada de AFD a AFN

---

### Código fuente

El repositorio contiene el código de una aplicación con interfaz gráfica que permite:

* Cargar autómatas
* Visualizar su estructura
* Validar cadenas de entrada

El código está organizado en carpetas para facilitar su comprensión y mantenimiento.

---

## Archivos completos de la práctica

Debido a los requerimientos de la entrega, los archivos completos del proyecto (incluyendo versiones comprimidas `.zip`) se encuentran disponibles en el siguiente enlace de Google Drive:

🔗 https://drive.google.com/file/d/1s7UsXH9mp0jdCbLuEvmIljsb8KmYEXFa/view?usp=sharing

Estos archivos incluyen:

* Autómatas en formato `.jff`, `.json` y `.xml`
* Código fuente completo
* Entorno de ejecución listo para usarse

---

## Instrucciones para ejecutar la práctica (entorno incluido)

Para facilitar la revisión, se incluye un entorno listo para ejecutar el proyecto sin necesidad de instalar múltiples versiones de JFLAP.

### Método recomendado 

1. Descargar el archivo `UL.zip` desde Google Drive
2. Extraer el contenido del archivo `.zip`
3. Abrir la carpeta `UL`
4. Ejecutar:

👉 Doble clic en:

```bash
setup.bat
```

---

### Método alternativo 

1. Abrir la carpeta `UL`

2. Abrir una terminal dentro de la carpeta:

   * Escribir `cmd` en la barra de direcciones y presionar Enter

3. Ejecutar:

```bash
python codigo.py
```

---

### Uso del programa

1. Ejecutar el programa
2. Cargar un archivo de autómata (`.jff`, `.json` o `.xml`)
3. Ingresar una cadena de prueba
4. Ejecutar la validación para verificar si la cadena es aceptada o rechazada

---

## Notas importantes

* El entorno incluido ya contiene las configuraciones necesarias
* No es necesario instalar JFLAP manualmente
* Asegurarse de tener Python instalado (versión 3.8 o superior)
* Ejecutar siempre desde la carpeta `UL`
* No modificar la estructura de carpetas del `.zip`

---

## Alcance de la práctica

* Este repositorio contiene únicamente la **Lista 2**
* La **Lista 3 (AFND y AFND-λ)** no está incluida
* Los autómatas fueron desarrollados en JFLAP y exportados a múltiples formatos

---

## Autores

* Perez Flores Arale
* Juarez Hipolito Marco Antonio
* Roque Villegas Ivan
