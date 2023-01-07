from selenium.webdriver.remote.webelement import WebElement

from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
import json
import os
import requests

class TiktokEntity(ABC):
    @abstractmethod
    def __post_init__(self):
        ...
        
    @abstractmethod
    def __repr__(self):
        ...
        
    @abstractmethod
    def to_dict(self):
        ...

@dataclass
class Author(TiktokEntity):
    """Model class representation of the user who posted the Tiktok video aka author.

    Args:
        uniqueid (str): Username of the author.
        avatar (str): Link to the avatar image of the author.
        link (str): Link to the profile of the author.
        nickname (str): Nickname of the author.
        element (WebElement): The Selenium web element which contains the details of the author. 
    """
    uniqueid: str
    avatar: str
    link: str
    nickname: str
    element: WebElement
    
    def __post_init__(self):
        self.uniqueid = self.uniqueid.strip()
        self.avatar = self.avatar.strip()
        self.link = self.link.strip()
        self.nickname = self.nickname.strip()
    
    def __eq__(self, obj) -> bool:
        return (self.uniqueid == obj.uniqueid) \
            and (self.link == obj.link)
            
    def __repr__(self):
        return f"Author(uniqueid={self.uniqueid}, nickname={self.nickname})"
    
    def to_dict(self):
        return dict(
            uniqueid=self.uniqueid,
            nickname=self.nickname,
            link=self.link,
            avatar=self.avatar,
            element=self.element.get_attribute("innerHTML")
        )

@dataclass
class Tag(TiktokEntity):
    """Model class representation of a tag in Tiktok. A tag or hashtag is a text preceded by a hash sign (#) which is used to categorize posts.

    Args:
        link (str): The link of the tag.
        text (str): The text of the tag.
        element (WebElement): The Selenium web element which contains the details of the tag. 
    """
    
    link: str
    text: str
    element: WebElement
    
    def __post_init__(self):
        self.link = self.link.strip()
        self.text = self.text.strip()
    
    def __eq__(self, obj) -> bool:
        return (self.text == obj.text) \
            and (self.link == obj.link)
            
    def __repr__(self):
        return f"Tag(link={self.link}, text={self.text})"
    
    def to_dict(self):
        return dict(
            link=self.link,
            text=self.text,
            element=self.element.get_attribute("innerHTML")
        )
    
@dataclass
class Caption(TiktokEntity):
    """Model class representation of the caption in a Tiktok video.

    Args:
        text (str): The caption in text format.
        tags (list[Tag]): List of tags inside the caption.
        element (WebElement): The Selenium web element which contains the details of the caption. 
    """
    text: str
    tags: list[Tag]
    element: WebElement

    def __post_init__(self):
        self.text = self.text.strip()
    
    def __repr__(self):
        return f"Caption(text={self.text}, tags={self.tags})"
    
    def to_dict(self):
        return dict(
            tags=[tag.to_dict() for tag in self.tags],
            text=self.text,
            element=self.element.get_attribute("innerHTML")
        )

@dataclass
class Music(TiktokEntity):
    """Model class representation of the music used in a Tiktok video.

    Args:
        title (str): The title of the music.
        link (str): The link of the music .
        element (WebElement): The Selenium web element which contains the details of the music. 
    """
    title: str
    link: str
    element: WebElement
    
    def __post_init__(self):
        self.title = self.title.strip()
        self.link = self.link.strip()
    
    def __eq__(self, obj) -> bool:
        return (self.title == obj.title) \
            and (self.link == obj.link)
    
    def __repr__(self):
        return f"Music(title={self.title}, link={self.link})"
    
    def to_dict(self):
        return dict(
            title=self.title,
            link=self.link,
            element=self.element.get_attribute("innerHTML")
        )

@dataclass
class Media(TiktokEntity):
    """Model class representation of the Tiktok video.

    Args:
        link (str): The link of the video.
        element (WebElement): The Selenium web element which contains the details of the video. 
    """
    link: str
    element: WebElement
    
    def __post_init__(self):
        self.link = self.link.strip()
    
    def __repr__(self):
        return f"Media(link={self.link})"
    
    def to_dict(self):
        return dict(
            link=self.link,
            element=self.element.get_attribute("innerHTML")
        )
    
@dataclass
class Metrics(TiktokEntity):
    """Model class representation of the metrics generated by the Tiktok video at a specific point of time.

    Args:
        likes (str): The raw number of likes extracted.
        comments (str): The raw number of comments extracted.
        shares (str): The raw number of shares extracted.
        element (WebElement): The Selenium web element which contains the metrics.
        as_of (str): The date time when the metrics are extracted in iso 8601 format. Defaults to the current date time.
    """
    likes: str
    comments: str
    shares: str
    element: WebElement
    as_of: str = datetime.datetime.now().isoformat()
    
    def __post_init__(self):
        self.likes = self.likes.strip()
        self.comments = self.comments.strip()
        self.shares = self.shares.strip()
    
    def __repr__(self):
        return f"Metrics(likes={self.likes}, comments={self.comments},shares={self.shares}, as_of={self.as_of} )"
    
    def to_dict(self):
        return dict(
            likes=self.likes,
            comments=self.comments,
            shares=self.shares,
            as_of=self.as_of,
            element=self.element.get_attribute("innerHTML")
        )

@dataclass
class Tiktok:
    """Model class representation of the Tiktok video to be extracted. This class utilizes all the other `entities` dataclasses.

    Args:
        id (str): Unique internal id of the Tiktok video.
        author (Author): `entities.Author` instance of the Tiktok video.
        caption (Caption): `entities.Caption` instance of the Tiktok video.
        music (Music): `entities.Music` instance of the Tiktok video.
        media (Media): `entities.Media` instance of the Tiktok video.
        metrics (Metrics): `entities.Metrics` instance of the Tiktok video.
        element (WebElement): The Selenium web element which contains the Tiktok video.
        status (str): A tag to signify if the scrape was sucessful. 
    """
    
    id: str
    author: Author
    caption: Caption
    music: Music
    media: Media
    metrics: Metrics
    element: WebElement
    status: str = None
    
    def save(self, path:str = "./"):
        def _save_metadata(path):
            file_path = os.path.join(path, f"{self.id}.json")
            with open(file_path, 'w+') as file:
                json.dump(self.to_dict(), file)
                
        def _save_video(path):
            file_path = os.path.join(path, f"{self.id}.mp4")
            response = requests.get(self.media.link)
            with open(file_path, "wb") as file:
                file.write(response.content)
        
        if self.media.link:
            _save_metadata(path)
            _save_video(path)
    
    def to_dict(self):
        return dict(
            id=self.id,
            Author=self.author.to_dict(),
            Caption=self.caption.to_dict(),
            Music=self.music.to_dict(),
            Media=self.media.to_dict(),
            Metrics=self.metrics.to_dict(),
            Element=self.element.get_attribute("innerHTML"),
            Status=self.status
        )

    def __eq__(self, obj) -> bool:
        return self.id == obj.id
    
    def __repr__(self) -> str:
        return f"Tiktok(id={self.id}, {self.status}, {self.author}, {self.caption}, {self.music}, {self.media}, {self.metrics})"
