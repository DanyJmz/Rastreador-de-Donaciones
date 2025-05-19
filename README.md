# Rastreador de Donaciones 

## Configuración

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Uso
1. Abre la interfaz Streamlit en tu navegador:
   ```
   http://localhost:8501
   ```
2. En la pestaña **Registrar una Donación**, ingresa los datos del donante.
3. En la pestaña **Registrar un Desembolso**, ingresa los detalles del desembolso.
4. Navega por las pestañas del **Panel de Control**:
   - **Donaciones**: historial de donaciones.
   - **Desembolsos**: historial de desembolsos.
   - **Blockchain**: registro completo de bloques para auditoría.
5. Para reiniciar la base de datos, elimina `donations.db` y reinicia la app.

## Estructura de archivos
- `blockchain.py`: lógica de la cadena de bloques.
- `models.py`: definiciones de modelo y base de datos.
- `app.py`: interfaz Streamlit.
- `requirements.txt`: dependencias.
- `README.md`: esta documentación.
