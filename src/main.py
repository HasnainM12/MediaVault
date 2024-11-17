import sys
import os
from typing import List, Dict, Callable
from src.models.media import Media
from src.database import Database
from src.api.tmdb import TMDBApi
from src.api.jikan import JikanApi

class MediaVault:
    def __init__(self):
        self.db = Database()
        self.tmdb = TMDBApi()
        self.media_list: List[Media] = self.db.load_data()
        self.jikan=JikanApi()
        

        self.commands: Dict[str, Callable] = {
            '1': self.view_all_media,
            '2': self.search_by_type,
            '3': self.add_media_from_tmdb,
            '4': self.view_media_details,
            '5': self.remove_media,
            '6': self.exit_program
        }
        
        self.menu_options: Dict[str, str] = {
            '1': "View all media",
            '2': "Search by type",
            '3': "Add media from TMDB",
            '4': "View media details",
            '5': "Remove media",
            '6': "Exit"
        }

    def save_changes(self) -> None:
        self.db.save_data(self.media_list)

    def display_menu(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== MediaVault ===")
        for key, value in self.menu_options.items():
            print(f"{key}. {value}")
        print("==================")

    def view_all_media(self) -> None:
        if not self.media_list:
            print("\nNo media found!")
            return
        
        print("\nCurrent Media List:")
        for i, media in enumerate(self.media_list, 1):
            print(f"{i}. {media.name} ({media.media_type})")
    
    def search_by_type(self) -> None:
        search_type = input("\nEnter media type to search (TV Show/Movie): ").strip()
        
        found = False
        print(f"\nResults for {search_type}:")
        for media in self.media_list:
            if media.media_type.lower() == search_type.lower():
                print(f"- {media.name}")
                found = True
        
        if not found:
            print("No matches found!")

    def search_tmdb(self, query: str, media_type: str) -> List[dict]:
        tmdb_type = "tv" if media_type.lower() == "tv show" else "movie"
        results = self.tmdb.search_media(query, tmdb_type)
        return results[:12]
    def display_search_results(self, results: List[dict]) -> None:

        if not results:
            print("\nNo results found!")
            return

        print("\nSearch Results:")
        for i, result in enumerate(results, 1):
            title = result.get("title") or result.get("name")
            year = ""
            if release_date := (result.get("release_date") or result.get("first_air_date")):
                year = f" ({release_date[:4]})"
            print(f"{i}. {title}{year}")

    def add_media_from_tmdb(self) -> None:

        media_type = input("\nEnter media type (TV Show/Movie): ").strip()
        if media_type.lower() not in ["tv show", "movie"]:
            print("Invalid media type!")
            return

        query = input("Enter search term: ").strip()
        if not query:
            print("Search term cannot be empty!")
            return

        results = self.search_tmdb(query, media_type)
        self.display_search_results(results)

        if results:
            try:
                choice = int(input("\nEnter number to add (0 to cancel): ")) - 1
                if 0 <= choice < len(results):
                    selected = results[choice]
                    tmdb_type = "tv" if media_type.lower() == "tv show" else "movie"
                    details = self.tmdb.get_details(selected["id"], tmdb_type)
                    
                    if details:
                        media = Media.from_tmdb_data(details, media_type)
                        self.media_list.append(media)
                        self.save_changes()
                        print(f"\n{media.name} has been added successfully!")
                elif choice != -1:
                    print("\nInvalid number!")
            except ValueError:
                print("\nPlease enter a valid number!")

    def add_new_media(self) -> None:
        print("\nSelect media type to add:")
        print("1. Movie")
        print("2. TV Show")
        print("3. Anime")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            self.add_media_from_tmdb("Movie")
        elif choice == '2':
            self.add_media_from_tmdb("TV Show")
        elif choice == '3':
            self.add_anime_from_jikan()
        else:
            print("\nInvalid choice!")

    def add_anime_from_jikan(self) -> None:
        query = input("\nEnter anime name to search: ").strip()
        if not query:
            print("Search term cannot be empty!")
            return

        results = self.jikan.search_anime(query)
        if not results:
            print("\nNo results found!")
            return

        print("\nSearch Results:")
        for i, anime in enumerate(results[:5], 1):
            year = f" ({anime['year']})" if anime.get('year') else ""
            print(f"{i}. {anime['title']}{year}")

        try:
            choice = int(input("\nEnter number to add (0 to cancel): ")) - 1
            if 0 <= choice < len(results[:5]):
                selected = results[choice]
                details = self.jikan.get_anime_details(selected['mal_id'])
                
                if details:
                    media = Media(
                        name=details['title'],
                        media_type="Anime",
                        overview=details.get('synopsis'),
                        release_date=str(details.get('year')),
                        rating=details.get('score'),
                        genres=[genre['name'] for genre in details.get('genres', [])]
                    )
                    self.media_list.append(media)
                    self.save_changes()
                    print(f"\n{media.name} has been added successfully!")
            elif choice != -1:
                print("\nInvalid number!")
        except ValueError:
            print("\nPlease enter a valid number!")

    def view_media_details(self) -> None:
        self.view_all_media()
        if not self.media_list:
            return

        try:
            index = int(input("\nEnter the number of the media to view (0 to cancel): ")) - 1
            if 0 <= index < len(self.media_list):
                media = self.media_list[index]
                print(f"\n=== {media.name} ===")
                print(f"Type: {media.media_type}")
                print(f"Added: {media.added_date}")
                if media.release_date:
                    print(f"Release Date: {media.release_date}")
                if media.rating:
                    print(f"Rating: {media.rating}/10")
                if media.genres:
                    print(f"Genres: {', '.join(media.genres)}")
                if media.overview:
                    print(f"\nOverview:\n{media.overview}")
            elif index != -1:
                print("\nInvalid number!")
        except ValueError:
            print("\nPlease enter a valid number!")

    def remove_media(self) -> None:
        self.view_all_media()
        if not self.media_list:
            return
            
        try:
            index = int(input("\nEnter the number of the media to remove (0 to cancel): ")) - 1
            if 0 <= index < len(self.media_list):
                removed = self.media_list.pop(index)
                self.save_changes()
                print(f"\n{removed.name} has been removed successfully!")
            elif index != -1:
                print("\nInvalid number!")
        except ValueError:
            print("\nPlease enter a valid number!")

    def exit_program(self) -> None:
        print("\nGoodbye!")
        sys.exit()

    def run(self) -> None:
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            action = self.commands.get(choice)
            if action:
                action()
                if choice != '6':
                    input("\nPress Enter to continue...")
            else:
                print("\nInvalid choice! Please try again.")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    vault = MediaVault()
    vault.run()