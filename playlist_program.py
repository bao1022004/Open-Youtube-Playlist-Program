import pygame
import webbrowser

class Video:
	def __init__(self, title, link):
		self.title = title
		self.link = link
		self.seen = False

	def open(self):
		webbrowser.open(self.link)
		self.seen = True

class Playlist:
	def __init__(self, name, description, rating, videos):
		self.name = name
		self.description = description
		self.rating = rating
		self.videos = videos

class TextButton:
	def __init__(self, text, position):
		self.text = text
		self.position = position
	def is_mouse_click(self):
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if mouse_x>self.position[0] and mouse_x<self.position[0]+self.text_box[2] and mouse_y>self.position[1] and mouse_y<self.position[1]+self.text_box[3]:
			return True
		return False
	def draw_button(self):
		font = pygame.font.SysFont('sans', 25)
		text_render = font.render(self.text,True,(0,0,0))
		self.text_box = text_render.get_rect()
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if self.is_mouse_click():
			text_render = font.render(self.text,True, (0,0,255))
			pygame.draw.line(screen,(0,0,255), (self.position[0],self.position[1]+self.text_box[3]),(self.position[0]+self.text_box[2],self.position[1]+self.text_box[3]))
		screen.blit(text_render,self.position)

def read_video_from_txt(file):
	title = file.readline()
	link = file.readline()
	video = Video(title, link)
	return video

def read_videos_from_txt(file):
	videos = []
	total = file.readline()		
	for i in range(int(total)):
		video = read_video_from_txt(file)
		videos.append(video)
	return videos

def read_playlist_from_txt(file):
	playlist_name = file.readline()
	playlist_description = file.readline()
	playlist_rating = file.readline()
	playlist_videos = read_videos_from_txt(file)
	playlist = Playlist(playlist_name, playlist_description, playlist_rating, playlist_videos)
	return playlist

def read_playlists_from_txt():
	playlists = []
	with open("data.txt", "r") as file:
		total = file.readline()
		for i in range(int(total)):
			playlist = read_playlist_from_txt(file)
			playlists.append(playlist)
	return playlists

def write_in_board(text,position):
	font = pygame.font.SysFont('sans', 25)
	text_render = font.render(text,True,(255,0,0))
	text_box = text_render.get_rect()
	screen.blit(text_render,position)

margin = 50
playlists = read_playlists_from_txt()

playlists_botton_list = []
for i in range(len(playlists)):
	playlist_button = TextButton(playlists[i].name.rstrip(),(50,60+i*margin))
	playlists_botton_list.append(playlist_button)

from random import randint
pygame.init()
screen = pygame.display.set_mode((600,400))
pygame.display.set_caption('Youtube Playlist')
running = True
WHITE= (255,255,255)
clock = pygame.time.Clock()
pygame.mouse.get_pos()

videos_button_list =[]
choice = None
while running:
	clock.tick(60)
	screen.fill(WHITE)
	write_in_board("Playlist",(50,20))
	write_in_board("Videos list",(250,20))
	#playlist_name_button.draw_button()
	for i in range (len(playlists_botton_list)):
		playlists_botton_list[i].draw_button()
	for i in range (len(videos_button_list)):
		videos_button_list[i].draw_button()

	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i in range(len(playlists_botton_list)):
					if playlists_botton_list[i].is_mouse_click():
						choice = i
						videos_button_list = []
						for j in range (len(playlists[i].videos)):
							video_button = TextButton(str(j+1) + "." + playlists[i].videos[j].title.rstrip(),(250,60+margin*j))
							videos_button_list.append(video_button)
				if choice!=None:					
					for i in range(len(videos_button_list)):
						if videos_button_list[i].is_mouse_click():
							playlists[choice].videos[i].open()
								
		if event.type == pygame.QUIT:
			running = False

	pygame.display.flip()
pygame.quit()