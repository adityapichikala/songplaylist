import pygame
import os
import time
import tkinter as tk
from tkinter import Label, Button, Listbox, END, Scale, HORIZONTAL

# Node class representing each song in the doubly linked list
class Node:
    def __init__(self, song_path):
        self.song_path = song_path  # Full file path to the song
        self.next = None  # Pointer to the next song
        self.prev = None  # Pointer to the previous song

# Playlist class that manages the doubly linked list
class Playlist:
    def __init__(self):
        self.head = None  # First song in the playlist
        self.tail = None  # Last song in the playlist
        self.current_song_node = None  # Pointer to the currently playing song
        pygame.mixer.init()  # Initialize pygame mixer for audio playback
        self.is_paused = False  # To track whether the song is paused

    # Add a song to the end of the playlist
    def add_song(self, song_path):
        if not os.path.exists(song_path):
            print(f"File '{song_path}' not found!")
            return

        new_node = Node(song_path)
        if not self.head:  # If playlist is empty
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node  # Link current tail to new node
            new_node.prev = self.tail  # Link new node back to current tail
            self.tail = new_node       # Update the tail to the new node
        print(f"Added: {os.path.basename(song_path)}")

    # Play a specific song
    def play_song(self, song_node):
        self.current_song_node = song_node
        pygame.mixer.music.load(song_node.song_path)  # Load the song
        pygame.mixer.music.play()  # Play the song
        self.is_paused = False  # Song is not paused
        print(f"Now playing: {os.path.basename(song_node.song_path)}")

    # Play the next song in the playlist
    def play_next(self):
        if self.current_song_node and self.current_song_node.next:
            self.play_song(self.current_song_node.next)
        else:
            print("Reached the end of the playlist.")

    # Play the previous song in the playlist
    def play_previous(self):
        if self.current_song_node and self.current_song_node.prev:
            self.play_song(self.current_song_node.prev)
        else:
            print("At the start of the playlist.")

    # Pause the currently playing song
    def pause_song(self):
        if not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            print("Paused the song.")

    # Resume the paused song
    def resume_song(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            print("Resumed the song.")

    # Stop the currently playing song
    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_paused = False
        print("Stopped playing.")

    # Set volume
    def set_volume(self, volume_level):
        pygame.mixer.music.set_volume(volume_level)

    # Check if the song is still playing
    def is_song_playing(self):
        return pygame.mixer.music.get_busy() and not self.is_paused

# GUI Class for controlling the playlist
class PlaylistGUI:
    def __init__(self, root, playlist):
        self.playlist = playlist
        self.root = root
        self.root.title("Music Player")

        # Playlist display
        self.song_list = Listbox(root, selectmode=tk.SINGLE, width=50, height=10)
        self.song_list.grid(row=0, column=0, columnspan=5)

        # Current song display
        self.current_song_label = Label(root, text="Now Playing: ", font=("Helvetica", 12, "bold"))
        self.current_song_label.grid(row=1, column=0, columnspan=5)

        # Buttons
        self.play_button = Button(root, text="Play", command=self.play_song, bg="lightgreen", width=10)
        self.play_button.grid(row=2, column=0)

        self.pause_button = Button(root, text="Pause", command=self.pause_song, bg="lightblue", width=10)
        self.pause_button.grid(row=2, column=1)

        self.resume_button = Button(root, text="Resume", command=self.resume_song, bg="lightyellow", width=10)
        self.resume_button.grid(row=2, column=2)

        self.next_button = Button(root, text="Next", command=self.play_next, bg="lightgray", width=10)
        self.next_button.grid(row=2, column=3)

        self.prev_button = Button(root, text="Previous", command=self.play_previous, bg="lightgray", width=10)
        self.prev_button.grid(row=2, column=4)

        # Volume control
        self.volume_scale = Scale(root, from_=0, to=1, resolution=0.1, orient=HORIZONTAL, label="Volume", command=self.change_volume)
        self.volume_scale.set(0.5)  # Default volume
        self.volume_scale.grid(row=3, column=0, columnspan=5)

        # Add songs to the playlist
        self.update_playlist_display()

    # Play the selected song from the list
    def play_song(self):
        selected_song_index = self.song_list.curselection()
        if selected_song_index:
            current_node = self.get_node_by_index(selected_song_index[0])
            self.playlist.play_song(current_node)
            self.update_current_song_display(current_node.song_path)
            self.highlight_current_song(selected_song_index[0])

    # Pause the current song
    def pause_song(self):
        self.playlist.pause_song()

    # Resume the current song
    def resume_song(self):
        self.playlist.resume_song()

    # Play the next song
    def play_next(self):
        if self.playlist.current_song_node and self.playlist.current_song_node.next:
            self.play_song_by_node(self.playlist.current_song_node.next)

    # Play the previous song
    def play_previous(self):
        if self.playlist.current_song_node and self.playlist.current_song_node.prev:
            self.play_song_by_node(self.playlist.current_song_node.prev)

    # Play a song by Node
    def play_song_by_node(self, song_node):
        self.playlist.play_song(song_node)
        self.update_current_song_display(song_node.song_path)
        current_index = self.get_index_by_node(song_node)
        self.highlight_current_song(current_index)

    # Update the current song display label
    def update_current_song_display(self, song_path):
        self.current_song_label.config(text=f"Now Playing: {os.path.basename(song_path)}")

    # Highlight the current song in the listbox
    def highlight_current_song(self, index):
        self.song_list.select_clear(0, END)  # Clear all selections
        self.song_list.select_set(index)  # Select the current song
        self.song_list.activate(index)  # Set focus to the current song

    # Update the song list display
    def update_playlist_display(self):
        self.song_list.delete(0, END)  # Clear the listbox
        current = self.playlist.head
        while current:
            self.song_list.insert(END, os.path.basename(current.song_path))
            current = current.next

    # Helper function to get node by index
    def get_node_by_index(self, index):
        current = self.playlist.head
        for _ in range(index):
            if current.next:
                current = current.next
        return current

    # Helper function to get index by node
    def get_index_by_node(self, node):
        current = self.playlist.head
        index = 0
        while current:
            if current == node:
                return index
            current = current.next
            index += 1
        return -1

    # Change volume using the scale
    def change_volume(self, value):
        volume_level = float(value)
        self.playlist.set_volume(volume_level)

# Example usage
if __name__ == "__main__":
    playlist = Playlist()

    # Add some songs to the playlist (replace with real file paths)
    playlist.add_song("C:/Users/Aditya/Downloads/[iSongs.info] 01 - Emitemitemito.mp3")
    playlist.add_song("C:/Users/Aditya/Downloads/128-Sunn Raha Hai (Male) - Aashiqui 2 128 Kbps.mp3")
    playlist.add_song("C:/Users/Aditya/Downloads/[iSongs.info] 04 - Telisiney Na Nuvvey.mp3")

    # Create the GUI
    root = tk.Tk()
    gui = PlaylistGUI(root, playlist)
    root.mainloop()

