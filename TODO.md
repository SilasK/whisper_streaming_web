# For running
caffeinate -t 7200 
mic input

ngrok http 5000 


# TODO
- [ ] Promt 200 char but only full words?
- [ ] Sentence that are not correctly endend and transcribed by a final dot.
- [ ] Ellipses, are some parts missing?
- [ ] Paragraph breaks
- [ ] Web interface has no space.
- [ ] Sentence stop doesn't care about "
- [ ] Break at least on comma



# Better VAC
- [x] + chunklenght to not have neg
- [x] Finalize should run a final translate.
- [ ] re init can be done many times !
- [ ] re init clears promt. But end of VAC is not always end of sentence.


# BEtter translations

- translation differ from time to time -> no exact match
- complete might be already in incomplete
- glitches if no audio -> VAC
- reprocess multiple times the same incompolete text

* Always keep last sentence in sentence segmentation?
* Don't translate part that is already there.. 

- [ ] Don't put empty or very short incomplete text


-  [ ] Filter low entropy text:
-  [ ] They come from finish!!
-  [ ] VAD could re-init before finished!!

"Ich habe Angst, den Widerspruch, die Jalousie, die Rivalitäten zu entdecken, der Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu Cu"


Pour faciliter notre exploration, je vais diviser le texte en quatre parties,! La raison pour la division un peu bizarre du texte en PowerPoint. Passons- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- Roh-bi- C'est parti !