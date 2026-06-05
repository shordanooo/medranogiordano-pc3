from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "documentacion.pdf")


class PDF(FPDF):
    def header(self):
        self.set_fill_color(26, 58, 107)
        self.rect(0, 0, 210, 18, "F")
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(255, 255, 255)
        self.set_xy(0, 4)
        self.cell(210, 10, "VOZ DEL CIUDADANO  |  Plataforma de Iniciativas Legislativas", align="C")
        self.set_text_color(0, 0, 0)
        self.ln(14)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Pagina {self.page_no()}", align="C")

    def h1(self, text):
        self.set_fill_color(26, 58, 107)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, f"  {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def h2(self, text):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(26, 58, 107)
        self.multi_cell(0, 6, text)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def para(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def kv(self, key, value):
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "B", 9)
        self.multi_cell(0, 5.5, key + ":")
        self.set_x(self.l_margin)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5.5, value)
        self.set_x(self.l_margin)
        self.ln(1)

    def row(self, cells, widths, header=False):
        fill_color = (208, 223, 245) if header else (245, 248, 255)
        self.set_fill_color(*fill_color)
        self.set_font("Helvetica", "B" if header else "", 9)
        for cell, w in zip(cells, widths):
            self.cell(w, 6, cell[:70], border=1, fill=True)
        self.ln()


def build():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(14, 22, 14)

    # PORTADA
    pdf.add_page()
    pdf.set_fill_color(26, 58, 107)
    pdf.rect(0, 0, 210, 297, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_xy(0, 75)
    pdf.cell(210, 14, "VOZ DEL CIUDADANO", align="C")
    pdf.ln(16)
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(210, 8, "Plataforma de Iniciativas Legislativas Ciudadanas", align="C")
    pdf.ln(12)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(210, 8, "Documentacion del Sistema - PC3  |  Diseno de Software", align="C")
    pdf.ln(38)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(210, 7, "Autores: Medrano  &  Giordano", align="C")
    pdf.ln(8)
    pdf.cell(210, 7, "Junio 2026", align="C")

    # 1. INTRODUCCION
    pdf.add_page()
    pdf.h1("1. INTRODUCCION")
    pdf.para(
        "El Legislativo de la Republica requiere el desarrollo de la plataforma digital "
        "'Voz del Ciudadano' para automatizar el procesamiento de Iniciativas Legislativas "
        "Ciudadanas. El software permite a colectivos civiles crear propuestas normativas y "
        "recolectar firmas digitales de apoyo.\n\n"
        "Al alcanzar el limite constitucional de 25 000 firmas digitales validas en un plazo "
        "maximo de 90 dias, el sistema congela criptograficamente el archivo (SHA-512) y lo "
        "envia automaticamente a la Oficina del Congreso para su distribucion a las comisiones "
        "parlamentarias. Los ciudadanos tambien pueden enviar comentarios, recursos de apoyo "
        "y modificaciones a las propuestas activas."
    )

    # 2. REQUISITOS FUNCIONALES
    pdf.h1("2. REQUISITOS FUNCIONALES")
    reqs = [
        ("RF-01", "Registro de Colectivo Civil", "Registrarse con nombre, DNI del representante y correo electronico."),
        ("RF-02", "Autenticacion de Usuarios", "Autenticacion mediante JWT. Las operaciones requieren sesion iniciada."),
        ("RF-03", "Creacion de Propuesta Legislativa", "Un colectivo autenticado crea una propuesta. El sistema asigna plazo de 90 dias."),
        ("RF-04", "Firma Digital de Propuesta", "Un ciudadano autenticado firma una propuesta activa. Una firma por DNI."),
        ("RF-05", "Control de Plazo de 90 Dias", "Verifica la fecha limite en cada firma. Propuestas vencidas pasan a EXPIRED."),
        ("RF-06", "Congelamiento Criptografico", "Al alcanzar 25 000 firmas genera hash SHA-512 y marca la propuesta FROZEN."),
        ("RF-07", "Envio al Congreso", "Tras el congelamiento envia el documento al Congreso y genera ticket de recepcion."),
        ("RF-08", "Gestion de Comentarios", "Los usuarios autenticados agregan comentarios de texto a propuestas activas."),
        ("RF-09", "Recursos de Apoyo", "Los usuarios adjuntan recursos (URL, titulo, tipo) que soportan la propuesta."),
        ("RF-10", "Consulta de Estado", "Cualquier visitante consulta: firmas, progreso %, dias restantes y hash SHA-512."),
    ]
    widths = [15, 48, 119]
    pdf.row(["ID", "Nombre", "Descripcion"], widths, header=True)
    for r in reqs:
        pdf.row(list(r), widths)
    pdf.ln(4)

    # 3. PATRONES ESTRUCTURALES
    pdf.h1("3. PATRONES ESTRUCTURALES IMPLEMENTADOS")
    pdf.h2("3.1 Patron Facade - VozCiudadanaFacade")
    pdf.para(
        "Proporciona una interfaz unificada y simplificada a los subsistemas de gestion de "
        "propuestas, recoleccion de firmas, congelamiento criptografico y envio al Congreso.\n\n"
        "Clase principal: app/patterns/facade.py -> VozCiudadanaFacade\n"
        "Metodos: create_proposal(), sign_proposal(), _freeze_and_submit(), get_proposal_status()\n\n"
        "Beneficio: Los routers de FastAPI solo interactuan con la Facade, ocultando la "
        "complejidad interna del CryptoService, CongressService y las validaciones."
    )
    pdf.h2("3.2 Patron Composite - LegislativeDocument")
    pdf.para(
        "Construye el documento legislativo como un arbol de componentes: titulo, resumen, "
        "texto completo y firmas. Permite calcular propiedades del conjunto (word_count) "
        "y serializar el documento para el congelamiento criptografico.\n\n"
        "Clases: ProposalComponent (abstracta), ProposalLeaf, ProposalComposite, LegislativeDocument\n"
        "Ubicacion: app/patterns/composite.py"
    )
    pdf.h2("3.3 Patron Decorator - Cadena de Validadores de Firma")
    pdf.para(
        "Anade capas de validacion en tiempo de ejecucion sin modificar la clase base.\n"
        "Cada decorador valida un aspecto especifico de la operacion de firma:\n"
        "  - DeadlineValidatorDecorator  : verifica que el plazo no haya vencido\n"
        "  - SignatureLimitDecorator     : verifica que no se hayan alcanzado 25 000 firmas\n"
        "  - DuplicateSignatureDecorator : verifica que el ciudadano no haya firmado antes\n"
        "  - StatusValidatorDecorator    : verifica que la propuesta este en estado COLLECTING\n\n"
        "La funcion build_signature_validator() compone la cadena completa.\n"
        "Ubicacion: app/patterns/decorator.py"
    )

    # 4. CASOS DE USO
    pdf.add_page()
    pdf.h1("4. CASOS DE USO")

    pdf.h2("CU-01: Crear Iniciativa Legislativa")
    items_cu01 = [
        ("Actor principal", "Representante de Colectivo Civil (usuario autenticado)"),
        ("Precondicion", "El usuario debe tener sesion iniciada (token JWT valido)."),
        ("Flujo principal",
         "1. El colectivo accede a 'Nueva Propuesta'.\n"
         "2. Ingresa titulo (min. 10 caracteres), resumen y texto completo.\n"
         "3. El sistema valida los datos mediante el schema ProposalCreate.\n"
         "4. La Facade crea la propuesta con status=COLLECTING y deadline=ahora+90 dias.\n"
         "5. El sistema retorna la propuesta creada con su ID."),
        ("Postcondicion", "La propuesta queda publicada y abierta para recibir firmas."),
        ("Flujo alternativo",
         "3a. Titulo < 10 caracteres -> HTTP 422 con mensaje de error.\n"
         "3b. Token JWT expirado -> HTTP 401 (no autorizado)."),
        ("Patrones involucrados", "Facade (create_proposal), Composite (LegislativeDocument)"),
    ]
    for k, v in items_cu01:
        pdf.kv(k, v)
    pdf.ln(2)

    pdf.h2("CU-02: Firmar una Propuesta Legislativa")
    items_cu02 = [
        ("Actor principal", "Ciudadano (usuario autenticado)"),
        ("Precondicion",
         "La propuesta existe, tiene status=COLLECTING, no ha expirado "
         "y el ciudadano no la ha firmado previamente."),
        ("Flujo principal",
         "1. El ciudadano accede al detalle de la propuesta.\n"
         "2. Hace clic en 'Firmar esta propuesta'.\n"
         "3. La Facade ejecuta la cadena de Decorators de validacion.\n"
         "4. Si todas las validaciones pasan, se registra la Signature en la BD.\n"
         "5. Se incrementa signature_count. Si llega a 25 000 -> flujo de congelamiento.\n"
         "6. El sistema retorna el nuevo conteo de firmas."),
        ("Postcondicion",
         "La firma queda registrada. Si se alcanzan 25 000, "
         "la propuesta es congelada y enviada al Congreso."),
        ("Flujo alternativo",
         "3a. Firma duplicada -> HTTP 400 'Ya firmaste esta propuesta'.\n"
         "3b. Plazo vencido -> HTTP 400 'La propuesta ha expirado'.\n"
         "3c. Propuesta congelada -> HTTP 400 'No se puede firmar'."),
        ("Patrones involucrados",
         "Facade (sign_proposal), Decorator (build_signature_validator), Composite (hash)"),
    ]
    for k, v in items_cu02:
        pdf.kv(k, v)
    pdf.ln(2)

    pdf.h2("CU-03: Consultar Estado de Propuesta")
    items_cu03 = [
        ("Actor principal", "Cualquier visitante (sin autenticacion requerida)"),
        ("Precondicion", "La propuesta debe existir en el sistema."),
        ("Flujo principal",
         "1. El visitante accede a la URL de detalle de la propuesta.\n"
         "2. El sistema llama a VozCiudadanaFacade.get_proposal_status().\n"
         "3. Si status=COLLECTING y deadline ya paso, el sistema actualiza a EXPIRED.\n"
         "4. Retorna: id, title, status, signature_count, signatures_needed, "
         "progress_percent, days_remaining, crypto_hash, congress_ticket."),
        ("Postcondicion",
         "El estado es devuelto al cliente. "
         "Si correspondia, la propuesta queda marcada como EXPIRED."),
        ("Flujo alternativo", "2a. Propuesta no encontrada -> HTTP 404."),
        ("Patrones involucrados", "Facade (get_proposal_status)"),
    ]
    for k, v in items_cu03:
        pdf.kv(k, v)
    pdf.ln(2)

    # 5. CASOS DE PRUEBA
    pdf.add_page()
    pdf.h1("5. CASOS DE PRUEBA")

    pdf.h2("CP-01: Creacion exitosa de propuesta legislativa")
    items_cp01 = [
        ("Objetivo", "Verificar que la Facade crea una propuesta con status=COLLECTING y plazo de 90 dias."),
        ("Precondicion", "Sistema iniciado. Usuario autenticado disponible."),
        ("Entrada",
         "title='Ley de Transparencia Digital', summary='...', full_text='...', author_id=1"),
        ("Pasos",
         "1. Invocar VozCiudadanaFacade.create_proposal() con los datos anteriores.\n"
         "2. Verificar el objeto retornado.\n"
         "3. Verificar que LegislativeDocument construye el arbol Composite correctamente."),
        ("Resultado esperado",
         "proposal.status == 'collecting'\n"
         "proposal.deadline aprox. utcnow + 90 dias\n"
         "LegislativeDocument.build() retorna 4 nodos hijo  |  total_words > 0"),
        ("Resultado", "PASS - TestCP01_CreacionPropuesta: todos los assertions pasan."),
        ("Archivo", "backend/tests/test_cases.py -> class TestCP01_CreacionPropuesta"),
    ]
    for k, v in items_cp01:
        pdf.kv(k, v)
    pdf.ln(2)

    pdf.h2("CP-02: Firma numero 25 000 activa congelamiento automatico")
    items_cp02 = [
        ("Objetivo",
         "Verificar que la firma 25 000 dispara el congelamiento criptografico "
         "y el envio al Congreso."),
        ("Precondicion", "Propuesta con signature_count=24 999, status=COLLECTING, plazo vigente."),
        ("Entrada", "proposal_id=1, citizen_id=42, ip_address='127.0.0.1'"),
        ("Pasos",
         "1. Crear mock de Proposal con signature_count=24 999.\n"
         "2. Invocar VozCiudadanaFacade.sign_proposal().\n"
         "3. Verificar que CryptoService genera el hash SHA-512.\n"
         "4. Verificar que CongressService.submit() retorna un ticket.\n"
         "5. Verificar el hash: 128 caracteres hexadecimales."),
        ("Resultado esperado",
         "result['success'] == True  |  '25,000' in result['message']\n"
         "len(result['crypto_hash']) == 128  |  result['congress_ticket'].startswith('CONGRESO-')"),
        ("Resultado", "PASS - TestCP02_CongelamientoAutomatico: todos los assertions pasan."),
        ("Archivo", "backend/tests/test_cases.py -> class TestCP02_CongelamientoAutomatico"),
    ]
    for k, v in items_cp02:
        pdf.kv(k, v)
    pdf.ln(2)

    pdf.h2("CP-03: Firma rechazada en propuesta expirada (90 dias vencidos)")
    items_cp03 = [
        ("Objetivo", "Verificar que el sistema rechaza firmas cuando el plazo de 90 dias ha vencido."),
        ("Precondicion", "Propuesta con deadline=ahora-1 dia, status=COLLECTING."),
        ("Entrada",
         "deadline=utcnow()-timedelta(days=1), signature_count=5000, citizen_id=10"),
        ("Pasos",
         "1. Construir la cadena de Decorators con build_signature_validator().\n"
         "2. Ejecutar validator.execute(data) con deadline expirado.\n"
         "3. Invocar get_proposal_status() con propuesta expirada hace 91 dias.\n"
         "4. Verificar que el estado cambia a EXPIRED."),
        ("Resultado esperado",
         "result['success'] == False  |  'expirado' in result['error']\n"
         "proposal.status == ProposalStatus.EXPIRED  |  days_remaining == 0"),
        ("Resultado", "PASS - TestCP03_PropuestaExpirada: todos los assertions pasan."),
        ("Archivo", "backend/tests/test_cases.py -> class TestCP03_PropuestaExpirada"),
    ]
    for k, v in items_cp03:
        pdf.kv(k, v)
    pdf.ln(2)

    # 6. ARQUITECTURA
    pdf.add_page()
    pdf.h1("6. ARQUITECTURA DEL SISTEMA")
    pdf.para(
        "Arquitectura de tres capas con separacion clara de responsabilidades:\n\n"
        "FRONTEND  (React JS, puerto 3000)\n"
        "  pages/      : Home, ProposalList, ProposalDetail, CreateProposal, Login, Register\n"
        "  components/ : Navbar, ProposalCard, SignatureCounter, CommentSection\n"
        "  services/   : api.js - llamadas HTTP con Axios + JWT\n\n"
        "BACKEND  (FastAPI + Python 3.13, puerto 8000)\n"
        "  routers/    : users.py, proposals.py (endpoints REST)\n"
        "  patterns/   : facade.py, composite.py, decorator.py\n"
        "  services/   : crypto_service.py, congress_service.py\n"
        "  models/     : SQLAlchemy ORM (User, Proposal, Signature, Comment, Resource)\n"
        "  schemas/    : Pydantic v2 (validacion de entrada/salida)\n"
        "  database.py : SQLite en desarrollo, configurable via DATABASE_URL\n\n"
        "BASE DE DATOS\n"
        "  SQLite para desarrollo, compatible con PostgreSQL en produccion."
    )

    pdf.h1("7. MODELO DE BRANCHING - GITFLOW")
    pdf.para(
        "Ramas del repositorio:\n\n"
        "  main                        : codigo en produccion\n"
        "  develop                     : integracion de funcionalidades\n"
        "  feature/backend-setup       : configuracion inicial FastAPI + modelos\n"
        "  feature/structural-patterns : Facade, Composite, Decorator\n"
        "  feature/frontend-react      : implementacion React JS\n"
        "  feature/tests               : casos de prueba pytest\n"
        "  release/1.0                 : preparacion del release final\n\n"
        "Repositorio: https://github.com/shordanooo/medranogiordano-pc3"
    )

    pdf.h1("8. INSTRUCCIONES DE EJECUCION")
    pdf.para(
        "BACKEND:\n"
        "  cd backend\n"
        "  pip install -r requirements.txt\n"
        "  cp .env.example .env\n"
        "  uvicorn app.main:app --reload --port 8000\n"
        "  Swagger UI: http://localhost:8000/docs\n\n"
        "FRONTEND:\n"
        "  cd frontend\n"
        "  npm install\n"
        "  npm start\n"
        "  Aplicacion: http://localhost:3000\n\n"
        "TESTS:\n"
        "  cd backend\n"
        "  pytest tests/ -v"
    )

    pdf.output(OUTPUT)
    print(f"PDF generado: {OUTPUT}")


if __name__ == "__main__":
    build()
