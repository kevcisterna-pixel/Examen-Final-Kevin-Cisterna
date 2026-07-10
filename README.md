# Examen Final Transversal: Tecnologías de Virtualización (DIY7111)

**Estudiante:** [Kevin Aaron Cisterna Fuentes]  
**Docente:** Rodrigo Horacio Aguilar González  
**Institución:** Duoc UC  
**Caso de Estudio:** Proyecto de Despliegue Stack Web - Empresa VZeta  
**Ponderación:** 40% de la Nota Final (Ejecución Práctica Individual)  

---

## 1. Justificación Técnica y Propuesta de Nube

### Justificación de Soluciones Contenerizadas (Docker/Compose) vs. Hipervisores Tradicionales
Para la empresa VZeta, implementar el stack de servicios utilizando Docker y Docker Compose presenta ventajas estratégicas e instrumentales críticas frente a la virtualización tradicional basada en hipervisores (como VMware ESXi, Proxmox o Hyper-V):

* **Eficiencia y Densidad de Recursos:** Los contenedores Docker no requieren un Sistema Operativo Invitado (Guest OS) completo ni emular hardware virtual, ya que comparten el Kernel del sistema operativo del host. Esto reduce el consumo de CPU y memoria RAM al mínimo, permitiendo que un entorno restringido como una instancia EC2 en AWS Learner Lab ejecute tres servicios en paralelo sin degradación de rendimiento.
* **Velocidad de Despliegue e Inicio:** El ciclo de vida de un contenedor se gestiona en milisegundos, puesto que levantar el proceso de la app Flask o la base de datos PostgreSQL no implica la secuencia de arranque (boot) que sí requiere una máquina virtual tradicional.
* **Licenciamiento y Costos Operativos (TCO):** Docker Engine y Docker Compose operan bajo licencias de código abierto (Open Source) sin costos asociados. Al compararlo con soluciones on-premise basadas en hipervisores tradicionales, se eliminan los complejos esquemas de pago por licenciamiento de cores, sockets o consolas de administración centralizadas, disminuyendo significativamente los costos operativos para VZeta.
* **Portabilidad Absoluta:** Al empaquetar el código, las dependencias (`requirements.txt`) y la configuración en una imagen propia basada en `python:3.12-slim`, garantizamos que el software se comportará exactamente igual en la máquina de desarrollo local que en la nube pública de AWS, eliminando el clásico problema de "en mi máquina sí funciona".

### Análisis de Entornos: Nube Pública, Privada e Híbrida
* **Nube Pública (Propuesta Seleccionada):** Se optó por desplegar la solución en la nube pública de **Amazon Web Services (AWS)**. Este entorno ofrece un modelo de pago por uso que reduce la inversión inicial de capital (CapEx) a cero. Dado que las restricciones técnicas actuales de VZeta no facultan el uso de orquestadores avanzados de alta disponibilidad (como Kubernetes o AWS EKS), el aprovisionamiento de una instancia EC2 administrada mediante Docker Compose cubre ágilmente las necesidades comerciales con bajo esfuerzo de mantenimiento.
* **Nube Privada:** Implementar una infraestructura privada (on-premise) con tecnologías tipo OpenStack o vSphere requeriría la adquisición de servidores físicos, almacenamiento local y personal dedicado a la mantención de hardware. Para este requerimiento web autocontenido, no es una alternativa viable económicamente.
* **Nube Híbrida:** Una arquitectura híbrida solo se justificaría si VZeta tuviese políticas de cumplimiento de datos que obligaran a almacenar la base de datos PostgreSQL en servidores físicos locales dentro de la empresa, manteniendo únicamente el proxy inverso y la app en la nube pública. Al ser una aplicación integrada sin dependencias heredadas críticas, centralizar el stack en la nube pública evita latencias de red innecesarias.

---

## 2. Descripción de la Arquitectura

El despliegue del stack se estructura mediante una topología multi-capa aislada dentro del Host de la siguiente forma:

```text
Cliente ── HTTP:80 ──> [ mynginx_container ] ──> [ myapp_container ] ──> [ db_container ]
                       (nginx reverse proxy)   (Flask · imagen propia) (PostgreSQL + volumen)
