def general_parser_individual_or_legal_entity(dictionary_pdf_texts):
    """Parse PDFs as either Individual or Legal Entity documents."""
    individual_parser = ProcessInputPDF()
    legal_entity_parser = LegalEntityPDFLoader()
    
    def parse_document(pdf_text, partner):
        """Try parsing as Individual, then Legal Entity."""
        # Try Individual
        if individual_parser.is_valid_document(pdf_text):
            try:
                individual_parser.check_substrings(pdf_text, individual_parser.required_substring_sets)
                processed = individual_parser.process_client_history(pdf_text)
                return {'type': 'individual', 'processed_client_history': processed, 
                       'individual': individual_parser.create_individual(processed)}
            except (MissingSubstringsError, Exception) as e:
                print(f'Error parsing individual ({partner}): {e}')
        
        # Try Legal Entity
        if legal_entity_parser.is_valid_document(pdf_text):
            try:
                processed = legal_entity_parser.process_client_history(pdf_text)
                return {'type': 'legal_entity', 'processed_client_history': processed,
                       'legal_entity': legal_entity_parser.create_individual(processed)}
            except Exception as e:
                print(f'Error parsing legal entity ({partner}): {e}')
        
        print(f'Invalid document for {partner}.')
        return None
    
    # Parse all documents with list comprehension
    parsed_br = {
        br: [result for partner, pdf_text in partners.items() 
             if (result := parse_document(pdf_text, partner)) is not None]
        for br, partners in dictionary_pdf_texts.items()
    }
    
    with open("parsed_br.json", "w") as f:
        json.dump(parsed_br, f, indent=2)
    
    return parsed_br