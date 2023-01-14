def get_phonetics(token, options={'aspirateLowTones': False}):

    '''Returns phonetics based on Khyentse Vision Project definition.
    
    token | str | a token to be converted into phonetics
    options | dict | a dictionary of option keys and their values
    
    '''
    
    from bophono.Converter import Converter

    converter = Converter(options=options)
    kvp_string = converter.get_api(token)
    
    return kvp_string