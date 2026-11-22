# Proyecto 1: Robot Ackermann (diseño mecánico)

| Carpeta / archivo | Contenido |
|---|---|
| `robot_ackermann_description/` | Paquete ROS 2 (Jazzy + Gazebo Harmonic): URDF/Xacro, mallas, launch, plugin Ackermann |
| `NOTAS_PERSONA2.md` | Cómo compilar y lanzar el paquete, joints, plugin y tópicos |
| `cad/robot_ackermann.f3d` | Modelo de Fusion 360 (piezas, ensamble, joints y parámetros) |
| `evidencias/` | Capturas del diseño (piezas, ensamble, dirección girada) |
| `planos/Planos_Robot_Ackermann.pdf` | Planos acotados A3 (3 hojas): ensamble con lista de piezas, chasis, rueda + mangueta |
| `documentacion/` | Sección de diseño mecánico para el informe IEEE (inglés) |

## Parámetros de diseño

| Parámetro | Valor |
|---|---|
| Distancia entre ejes (L) | 300 mm |
| Ancho de vía (centro a centro de ruedas) | 220 mm |
| Distancia entre pivotes de dirección | 160 mm |
| Rueda | Ø100 × 30 mm |
| Giro máximo del robot | 30° → radio de giro mínimo ≈ 0.52 m |
| Límite de cada mangueta | ±35° (rueda interior ≈ 34.3° a 30°) |
| Chasis | 400 × 110 × 6 mm, aluminio 6061 |
| Masa total | ≈ 1.83 kg |
