from flask import Flask, request, jsonify, render_template
import stanza
from stanza import DownloadMethod
from stanza.utils.conll import CoNLL

def create_conll_html_string(conll):
    conll_prints = []

    # takes in query sentence
    # returns a list containing the brat html for each and every sentence
    for sentence in conll:
        cur_sen = ""
        for word in sentence:
            for index, item in enumerate(word):
                if index == len(word) - 1:
                    cur_sen += item
                else:
                    cur_sen += item + "\t"
            cur_sen += "\n"
            
        conll_out_sen = f"""<pre><code class="language-conllu"># visual-style 5 2 nsubj:pass	color:blue
# visual-style 4 7 obl	color:blue
{cur_sen}
</code></pre>"""

        conll_prints.append(conll_out_sen)
        
    return conll_prints

def generate_brat(model, query):
    # select models first
    # then input sentences
    # e.g. 这是一句话。 快速的棕色狐狸跳过了懒惰的狗。这是最后一句话?
    doc = None
    if model == 'LTP':
        doc = nlp_LTP(str(query))
    elif model == 'Penn':
        doc = nlp_Penn(str(query))
    elif model == 'PKU':
        doc = nlp_PKU(str(query))
    elif model == 'GSD':
        doc = nlp_GSD(str(query))
    elif model == 'spaCy':
        doc = nlp_spaCy(str(query))

    # dependency parsing, convert results to conll format, then format into html strings
    conll_prints = ""
    og_sentences = []
    if doc != None:
        for sentence in doc.sentences:
            og_sentences.append(str(sentence.text))
        dicts = doc.to_dict() 
        conll = CoNLL.convert_dict(dicts) 
        conll_prints = create_conll_html_string(conll)

    return og_sentences, conll_prints

# -----------------------------------------------------------------------------------------------------------------

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', content="")

@app.route('/', methods=['GET','POST'])
def process():
    query = request.form.get('textInput', 'No Content')
    selected_models = request.form.getlist('checkbox')
    selected_view = request.form.getlist('viewby')

    coll_print_html = ""
    # view by model: [model_id, all_sentences_output_by_model]
    model_sentence_htmls = []
    # view by sentence: [sentence_id, model_id, sentence_model_output]
    model_sentence_htmls_dict = {}
    original_sentence = []

    # view output by model
    if selected_view[0] == "model":
        # process sentences for each model selected
        for model in selected_models:
            # generate brat html for query sentences
            og_sentences, conll_prints = generate_brat(model, query)
            model_sentence_htmls.append((model, conll_prints))

        # for each model
        for result_by_model in model_sentence_htmls:
            model = result_by_model[0]
            conll_prints = result_by_model[1]
            # append brat html to format html string
            coll_print_html += f"<hr class='page_divider'><label>{model}</label>" + "\n"
            for coll_prt in conll_prints:
                coll_print_html += coll_prt + "\n" 
        coll_print_html += "<hr class='page_divider'>"

    else: # view output by sentence
        # process sentences for each model selected
        for model in selected_models:
            # generate brat html for query sentences
            og_sentences, conll_prints = generate_brat(model, query)
            original_sentence = og_sentences
            # store every sentence in dict
            for sentence_id, coll_prt in enumerate(conll_prints):
                key = str(sentence_id)
                if key not in model_sentence_htmls_dict.keys():
                    model_sentence_htmls_dict[key] = [(model, coll_prt)]
                else:
                    model_sentence_htmls_dict[key].append((model, coll_prt))

        # for each sentence
        for sentence_id_key in model_sentence_htmls_dict.keys():
            # a list of (mode, sentence html) pairs for the current sentence
            html_prints_by_sen = model_sentence_htmls_dict[sentence_id_key]
            # add every sentence to final html string
            # coll_print_html += f"<label style='font-weight: normal;'> \
            #                         Original Sentence: {original_sentence[int(sentence_id_key)]} \
            #                     </label>" + "\n"
            coll_print_html += "<hr class='page_divider'><div style='display: flex;'> \
                                    <div style='display: inline-block; align-content: center; width: 5%;'> \
                                    <label>Input</label> \
                                    </div> \
                                    <div style='display: inline-block; width: 95%;'>" \
                                    + "\n" + f"<p>{original_sentence[int(sentence_id_key)]}</p>" + "\n" + "</div></div>"

            for index, coll_model_pair in enumerate(html_prints_by_sen):
                model = coll_model_pair[0]
                coll_prt = coll_model_pair[1]
                coll_print_html += f"<div style='display: flex;'> \
                                        <div style='display: inline-block; align-content: center; width: 5%;'> \
                                        <label>{model}</label> \
                                        </div> \
                                        <div style='display: inline-block; width: 95%;'>" \
                                        + "\n"
                coll_print_html += coll_prt + "\n" + "</div></div>"
                if index < len(html_prints_by_sen) - 1:
                    coll_print_html += "<hr>"
        coll_print_html += "<hr class='page_divider'>\n"

    return render_template(
        'index.html', 
        content=coll_print_html, 
        selected_models=selected_models, 
        query=query,
        selected_view=selected_view)

# -----------------------------------------------------------------------------------------------------------------
    
if __name__ == '__main__':
    # loading models into stanza

    nlp_LTP = stanza.Pipeline(
        lang="zh-hans",
        download_method=DownloadMethod.REUSE_RESOURCES,
        depparse_model_path="models/UD_Chinese-GSDLTP/UD_Chinese-GSDSimp_model/saved_models/depparse/zh-hans_gsdsimp_electra-large_parser.pt",
        pos_model_path="models/UD_Chinese-GSDLTP/UD_Chinese-GSDSimp_model/saved_models/pos/zh-hans_gsdsimp_charlm_tagger.pt",
        tokenize_model_path="models/UD_Chinese-GSDLTP/UD_Chinese-GSDSimp_model/saved_models/tokenize/zh-hans_gsdsimp_tokenizer.pt",
        processors='tokenize,pos,lemma,depparse', )

    # nlp_Penn = stanza.Pipeline(
    #     lang="zh-hans",
    #     download_method=DownloadMethod.REUSE_RESOURCES,
    #     depparse_model_path="models/UD_Chinese-GSDPenn/UD_Chinese-GSDSimp_model/saved_models/depparse/zh-hans_gsdsimp_electra-large_parser.pt",
    #     pos_model_path="models/UD_Chinese-GSDPenn/UD_Chinese-GSDSimp_model/saved_models/pos/zh-hans_gsdsimp_charlm_tagger.pt",
    #     tokenize_model_path="models/UD_Chinese-GSDPenn/UD_Chinese-GSDSimp_model/saved_models/tokenize/zh-hans_gsdsimp_tokenizer.pt",
    #     processors='tokenize,pos,lemma,depparse', )

    # nlp_PKU = stanza.Pipeline(
    #     lang="zh-hans",
    #     download_method=DownloadMethod.REUSE_RESOURCES,
    #     depparse_model_path="models/UD_Chinese-GSDPKU/UD_Chinese-GSDSimp_model-charlm/saved_models/depparse/zh-hans_gsdsimp_charlm_parser.pt",
    #     pos_model_path="models/UD_Chinese-GSDPKU/UD_Chinese-GSDSimp_model-charlm/saved_models/pos/zh-hans_gsdsimp_charlm_tagger.pt",
    #     tokenize_model_path="models/UD_Chinese-GSDPKU/UD_Chinese-GSDSimp_model-charlm/saved_models/tokenize/zh-hans_gsdsimp_tokenizer.pt",
    #     processors='tokenize,pos,lemma,depparse', )

    nlp_GSD = stanza.Pipeline(
        lang="zh-hans",
        download_method=DownloadMethod.REUSE_RESOURCES,
        depparse_model_path="models/UD_Chinese-GSDSimp/UD_Chinese-GSDSimp_model/saved_models/depparse/zh-hans_gsdsimp_electra-large_parser.pt",
        pos_model_path="models/UD_Chinese-GSDSimp/UD_Chinese-GSDSimp_model/saved_models/pos/zh-hans_gsdsimp_charlm_tagger.pt",
        tokenize_model_path="models/UD_Chinese-GSDSimp/UD_Chinese-GSDSimp_model/saved_models/tokenize/zh-hans_gsdsimp_tokenizer.pt",
        processors='tokenize,pos,lemma,depparse', )

    # nlp_spaCy = stanza.Pipeline(
    #     lang="zh-hans",
    #     download_method=DownloadMethod.REUSE_RESOURCES,
    #     depparse_model_path="models/UD_Chinese-GSDspaCy/UD_Chinese-GSDSimp_model-charlm/saved_models/depparse/zh-hans_gsdsimp_charlm_parser.pt",
    #     pos_model_path="models/UD_Chinese-GSDspaCy/UD_Chinese-GSDSimp_model-charlm/saved_models/pos/zh-hans_gsdsimp_charlm_tagger.pt",
    #     tokenize_model_path="models/UD_Chinese-GSDspaCy/UD_Chinese-GSDSimp_model-charlm/saved_models/tokenize/zh-hans_gsdsimp_tokenizer.pt",
    #     processors='tokenize,pos,lemma,depparse', )

    app.run(debug=False)
