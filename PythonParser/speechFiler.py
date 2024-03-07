def speech_file(mytext="Hello World",slow_val=0, output_file="output", tld_val="com"):
    # Import the required module for text
    # to speech conversion
    from gtts import gTTS

    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=slow_val, tld=tld_val)

    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save(output_file)