
def general_parser_individual_or_legal_entity(dictionary_pdf_texts):
    """Parse PDFs as either Individual or Legal Entity documents."""
    parsed_br = {}
    
    # Initialize parsers once
    individual_parser = ProcessInputPDF()
    legal_entity_parser = LegalEntityPDFLoader()
    
    for br in dictionary_pdf_texts.keys():
        parsed_br[br] = []
        
        for partner, pdf_text in dictionary_pdf_texts[br].items():
            parsed_entity = _try_parse_document(
                pdf_text, 
                partner, 
                individual_parser, 
                legal_entity_parser
            )
            
            if parsed_entity:
                parsed_br[br].append(parsed_entity)
    
    _save_to_json(parsed_br, "parsed_br.json")
    return parsed_br


def _try_parse_document(pdf_text, partner, individual_parser, legal_entity_parser):
    """Try parsing as Individual first, then Legal Entity."""
    
    # Try Individual
    result = _try_individual_parse(pdf_text, partner, individual_parser)
    if result:
        return result
    
    # Try Legal Entity
    result = _try_legal_entity_parse(pdf_text, partner, legal_entity_parser)
    if result:
        return result
    
    print(f'Could not parse document for {partner}')
    return None


def _try_individual_parse(pdf_text, partner, parser):
    """Attempt to parse as Individual document."""
    try:
        if not parser.is_valid_document(pdf_text):
            return None
        
        parser.check_substrings(pdf_text, parser.required_substring_sets)
        processed_history = parser.process_client_history(pdf_text)
        individual = parser.create_individual(processed_history)
        
        return {
            'type': 'individual',
            'processed_client_history': processed_history,
            'individual': individual
        }
    
    except MissingSubstringsError:
        print(f'Missing required substrings for individual in {partner}.')
        return None
    except Exception as e:
        print(f'Error parsing as individual ({partner}): {e}')
        return None


def _try_legal_entity_parse(pdf_text, partner, parser):
    """Attempt to parse as Legal Entity document."""
    try:
        if not parser.is_valid_document(pdf_text):
            return None
        
        processed_history = parser.process_client_history(pdf_text)
        legal_entity = parser.create_individual(processed_history)  # or create_legal_entity if different
        
        return {
            'type': 'legal_entity',
            'processed_client_history': processed_history,
            'legal_entity': legal_entity
        }
    
    except Exception as e:
        print(f'Error parsing as legal entity ({partner}): {e}')
        return None


def _save_to_json(data, filename):
    """Save parsed data to JSON file."""
    try:
        with open(filename, "w") as json_parsed:
            json.dump(data, json_parsed, indent=2)
        print(f'Successfully saved to {filename}')
    except Exception as e:
        print(f'Error saving to JSON: {e}')