# Explicação do Formato iCalendar (.ics)

Este arquivo `.ics` segue o padrão **iCalendar** especificado pela **RFC 5545**. Ele é utilizado para agendar eventos em aplicativos de calendário. Abaixo, explicamos cada item do template e fornecemos um exemplo já preenchido.

## Descrição

ICS é a extensão de arquivos no formato **iCalendar**, utilizado para agendar, compartilhar e importar eventos em aplicativos de calendário como Google Calendar e Outlook. Ele segue o padrão definido pela **RFC 5545**.

## **Template Original**

```plaintext
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//appsheet.com//appsheet 1.0//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
SUMMARY:Invitation from <<USEREMAIL()>> to talk about <<[MeetingTopic]>>
UID:c7614cff-3549-4a00-9152-d25cc1fe077d
SEQUENCE:0
STATUS:CONFIRMED
TRANSP:TRANSPARENT
DTSTART:<<[StartDateTime]>>
DTEND:<<[EndDateTime]>>
LOCATION:<<[MeetingAddress]>>
DESCRIPTION:<<[MeetingDescription]>>
END:VEVENT
END:VCALENDAR
```

## **Exemplo Preenchido**

```plaintext
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//appsheet.com//appsheet 1.0//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
SUMMARY:Invitation from john.doe@example.com to talk about Project Updates
UID:12345678-90ab-cdef-1234-567890abcdef
SEQUENCE:0
STATUS:CONFIRMED
TRANSP:TRANSPARENT
DTSTART:20250130T150000Z
DTEND:20250130T160000Z
LOCATION:Conference Room 1, Main Office
DESCRIPTION:Discussion about the current status of the project and next steps.
END:VEVENT
END:VCALENDAR
```

## **Descrição de Cada Campo**

### **Cabeçalho do Calendário**

- `BEGIN:VCALENDAR`: Define o início de um calendário no arquivo.
- `VERSION:2.0`: Especifica a versão do formato iCalendar utilizada.
- `PRODID:-//appsheet.com//appsheet 1.0//EN`: Identifica o software que gerou o arquivo.  
  - **Exemplo Preenchido**: `-//appsheet.com//appsheet 1.0//EN`
- `CALSCALE:GREGORIAN`: Especifica o uso do calendário gregoriano.
- `METHOD:PUBLISH`: Indica que o evento está sendo publicado (não enviado como convite).

### **Evento**

- `BEGIN:VEVENT`: Define o início de um evento.
- `SUMMARY`: Resumo ou título do evento.  
  - **Exemplo Preenchido**: `Invitation from john.doe@example.com to talk about Project Updates`
- `UID`: Identificador único do evento, usado para evitar duplicações.  
  - **Exemplo Preenchido**: `12345678-90ab-cdef-1234-567890abcdef`
- `SEQUENCE`: Número da revisão do evento. Incrementa quando há atualizações.  
  - **Exemplo Preenchido**: `0`
- `STATUS`: Status do evento (ex.: `CONFIRMED`, `TENTATIVE`, `CANCELLED`).  
  - **Exemplo Preenchido**: `CONFIRMED`
- `TRANSP`: Define se o evento bloqueia o tempo no calendário.  
  - **Opções**: `TRANSPARENT` (não bloqueia) ou `OPAQUE` (bloqueia).  
  - **Exemplo Preenchido**: `TRANSPARENT`
- `DTSTART`: Data e hora de início do evento (formato UTC: `YYYYMMDDTHHMMSSZ`).  
  - **Exemplo Preenchido**: `20250130T150000Z` (30/01/2025, 15:00 UTC)
- `DTEND`: Data e hora de término do evento (formato UTC: `YYYYMMDDTHHMMSSZ`).  
  - **Exemplo Preenchido**: `20250130T160000Z` (30/01/2025, 16:00 UTC)
- `LOCATION`: Local do evento.  
  - **Exemplo Preenchido**: `Conference Room 1, Main Office`
- `DESCRIPTION`: Descrição detalhada do evento.  
  - **Exemplo Preenchido**: `Discussion about the current status of the project and next steps.`
- `END:VEVENT`: Define o fim de um evento.

### **Rodapé do Calendário**

- `END:VCALENDAR`: Define o fim do arquivo de calendário.

---

## **Notas**

- **Placeholders**: Campos entre `<< >>` no template original serão substituídos por valores reais quando o arquivo for gerado.
- **Formato de Data e Hora**: `DTSTART` e `DTEND` seguem o formato ISO 8601:
  - `YYYYMMDD`: Ano, mês e dia.
  - `T`: Separador entre data e hora.
  - `HHMMSS`: Horas, minutos e segundos.
  - `Z`: Indica que o horário está em UTC (Tempo Universal Coordenado).

Para mais detalhes, consulte a [RFC 5545](https://datatracker.ietf.org/doc/html/rfc5545).
