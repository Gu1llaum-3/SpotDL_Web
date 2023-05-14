from flask import Flask, request, send_file, render_template
from subprocess import run
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/', methods=['GET', 'POST'])
def download_file():
    session_id = secrets.token_hex(16)
    download_param_album = '{artist}/{album}/{artist} - {title}'
    download_param_playlist = '{playlist}/{artists}/{album} - {title} {artist}'
    download_param_track = '{artist}/{album}/{artist} - {title}'

    if request.method == 'POST':
        url1 = request.form['url1']
        url2 = request.form['url2']
        url3 = request.form['url3']
        url4 = request.form['url4']
        url5 = request.form['url5']

        # Vérifier si au moins un champ est vide
        if not url1 and not url2 and not url3 and not url4 and not url5:
            return render_template('erreur.html')

        urls = [url1, url2, url3, url4, url5]
  
        # Créer le dossier 'downloads' s'il n'existe pas
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        os.chdir('downloads')
        os.system(f'rm -rf *')

        for url in urls:
            if url:
                if "album" in url:
                    run(['python3', '-m', 'spotdl', url, '--output', download_param_album])
                elif "playlist" in url:
                    run(['python3', '-m', 'spotdl', url, '--output', download_param_playlist])
                elif "track" in url:
                    run(['python3', '-m', 'spotdl', url, '--output', download_param_track])
        
        run(['zip', '-r', 'musics.zip', '.'])
        os.chdir('../')

        path = "downloads/musics.zip"
        return send_file(path, as_attachment=True)

    return render_template('index.html')


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=3000)
