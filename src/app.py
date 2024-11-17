from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database
from api.tmdb import TMDBApi
from api.jikan import JikanApi
from models.media import Media



app = Flask(__name__)



db = Database()
tmdb = TMDBApi()
jikan = JikanApi()

@app.route('/')
def index():
    media_list = db.load_data()
    return render_template('index.html', media_list=media_list)

@app.route('/search', methods=['GET'])
def search():
    media_type = request.args.get('type', 'movie')
    query = request.args.get('query', '')
    results = []
    
    if query:
        if media_type in ['movie', 'tv']:
            results = tmdb.search_media(query, media_type)[:5]
        elif media_type == 'anime':
            results = jikan.search_anime(query)[:5]
    
    return render_template('search.html', results=results, media_type=media_type, query=query)

@app.route('/add', methods=['POST'])
def add_media():
    media_type = request.form.get('type')
    media_id = request.form.get('id')
    
    if media_type in ['movie', 'tv']:
        details = tmdb.get_details(int(media_id), media_type)
        if details:
            media = Media.from_tmdb_data(details, 'Movie' if media_type == 'movie' else 'TV Show')
    elif media_type == 'anime':
        details = jikan.get_anime_details(int(media_id))
        if details:
            media = Media(
                name=details['title'],
                media_type="Anime",
                overview=details.get('synopsis'),
                release_date=str(details.get('year')),
                rating=details.get('score'),
                genres=[genre['name'] for genre in details.get('genres', [])]
            )
    
    media_list = db.load_data()
    media_list.append(media)
    db.save_data(media_list)
    flash(f'Successfully added {media.name}!')
    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_media(index):
    media_list = db.load_data()
    if 0 <= index < len(media_list):
        deleted = media_list.pop(index)
        db.save_data(media_list)
        flash(f'Successfully removed {deleted.name}!')
    return redirect(url_for('index'))



@app.route('/media/<int:index>')
def view_media(index):
    media_list = db.load_data()
    if 0 <= index < len(media_list):
        media = media_list[index]
        return render_template('media_detail.html', media=media, index=index)
    flash('Media not found!')
    return redirect(url_for('index'))

@app.route('/media/<int:index>/review', methods=['POST'])
def add_review(index):
    media_list = db.load_data()
    if 0 <= index < len(media_list):
        try:
            rating = float(request.form.get('rating', 0))
            if not (0 <= rating <= 10):
                raise ValueError("Rating must be between 0 and 10")
            
            review = request.form.get('review', '').strip()
            
            media_list[index].add_review(rating, review)
            db.save_data(media_list)
            
            flash('Review added successfully!')
        except ValueError as e:
            flash(f'Error: {str(e)}')
        return redirect(url_for('view_media', index=index))
    
    flash('Media not found!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)