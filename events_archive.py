#!/usr/bin/env python3
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict

class EventsArchiveGenerator:
    def __init__(self):
        # Archive events will use IDs starting from 100,000 to avoid conflicts with generate_events.py (IDs 1-10,000)
        self.archive_id_start = 100000
        
        self.event_types = ["film", "game", "cinema", "concert", "theater", "sport", "exhibition"]
        self.providers = ["TicketRu", "EventWorld", "ShowTime", "CultureCity", "SportHub"]
        
        self.film_titles = [
            "Тайна старого города", "Зеленая миля", "Алые паруса", "Белые ночи",
            "Черный квадрат", "Золотая осень", "Синяя птица", "Красная шапочка",
            "Звездные войны", "Матрица", "Титаник", "Аватар", "Гладиатор"
        ]
        
        self.game_shows = [
            "Форт Боярд", "Своя игра", "Что? Где? Когда?", "Поле чудес",
            "Кто хочет стать миллионером?", "Умники и умницы", "Брейн ринг"
        ]
        
        self.names = [
            "Андрей Смирнов", "Владимир Смирнов", "Анна Иванов", "Михаил Петров",
            "Елена Смирнов", "Дмитрий Козлов", "Ольга Сидорова", "Алексей Морозов",
            "Татьяна Волкова", "Сергей Лебедев", "Мария Соколова", "Николай Орлов"
        ]
        
        self.descriptions = [
            "Захватывающее представление, которое оставит неизгладимые воспоминания. Профессиональные актеры и великолепная постановка.",
            "Уникальное мероприятие для всей семьи. Не пропустите яркое шоу с участием известных артистов и незабываемые впечатления.",
            "Развлекательная программа для всех возрастов. Веселье, смех и позитивные эмоции обеспечены каждому зрителю.",
            "Культурное событие высочайшего уровня. Изысканная программа для истинных ценителей искусства и прекрасного.",
            "Незабываемое шоу с потрясающими спецэффектами. Мастерство исполнителей поразит даже самых требовательных зрителей.",
            "Увлекательное мероприятие для любителей интеллектуальных развлечений. Атмосфера азарта и соперничества гарантирована.",
            "Грандиозное событие, которое станет настоящим праздником для души. Яркие эмоции и восторженные отзывы публики."
        ]

    def generate_event_title(self, event_type: str) -> str:
        if event_type == "film":
            title_base = random.choice(self.film_titles)
            person = random.choice(self.names)
            templates = [
                f'Премьера фильма "{title_base}" с участием {person}',
                f'Показ картины "{title_base}" с {person} в главной роли',
                f'Киносеанс "{title_base}" режиссера {person}',
                f'Кинопоказ "{title_base}" в честь {person}'
            ]
        elif event_type == "game":
            show = random.choice(self.game_shows)
            host = random.choice(self.names)
            templates = [
                f'Игровое шоу "{show}" с ведущим {host}',
                f'Телешоу "{show}" при участии {host}',
                f'Интеллектуальная игра "{show}" с {host}'
            ]
        elif event_type == "cinema":
            title_base = random.choice(self.film_titles)
            person = random.choice(self.names)
            templates = [
                f'Кинопоказ "{title_base}" в честь {person}',
                f'Киномарафон "{title_base}" с {person}',
                f'Ретроспектива "{title_base}" посвященная {person}'
            ]
        elif event_type == "concert":
            person = random.choice(self.names)
            templates = [
                f'Концерт {person}',
                f'Сольный концерт {person}',
                f'Музыкальный вечер с {person}',
                f'Гала-концерт {person}'
            ]
        elif event_type == "theater":
            title_base = random.choice(self.film_titles)
            person = random.choice(self.names)
            templates = [
                f'Спектакль "{title_base}" с {person}',
                f'Театральная постановка "{title_base}" при участии {person}',
                f'Премьера спектакля "{title_base}" с {person} в главной роли'
            ]
        elif event_type == "sport":
            person = random.choice(self.names)
            templates = [
                f'Спортивное соревнование с участием {person}',
                f'Турнир памяти {person}',
                f'Чемпионат города при поддержке {person}'
            ]
        else:  # exhibition
            person = random.choice(self.names)
            templates = [
                f'Выставка работ {person}',
                f'Персональная выставка {person}',
                f'Экспозиция "{random.choice(self.film_titles)}" куратор {person}'
            ]
        
        return random.choice(templates)

    def generate_datetime(self, start_date: datetime, end_date: datetime) -> str:
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        random_date = start_date + timedelta(days=random_days)
        
        # Generate random time (mostly evening hours for events)
        hour = random.choices(
            [17, 18, 19, 20, 21, 22],
            weights=[10, 20, 30, 25, 10, 5]
        )[0]
        minute = random.choice([0, 15, 30, 45])
        
        random_datetime = random_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        return random_datetime.isoformat()

    def generate_events(self, count: int, start_year: int = 2015, end_year: int = 2024) -> List[Dict]:
        events = []
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        
        print(f"Generating {count:,} archive events from {start_year} to {end_year}...")
        print(f"Archive events will have IDs starting from {self.archive_id_start:,}")
        print(f"ID range: {self.archive_id_start:,} to {self.archive_id_start + count - 1:,}")
        
        for i in range(count):
            if (i + 1) % 100000 == 0:
                print(f"Generated {i + 1:,} events...")
            
            event_type = random.choice(self.event_types)
            
            event = {
                "id": self.archive_id_start + i,
                "title": self.generate_event_title(event_type),
                "description": random.choice(self.descriptions),
                "type": event_type,
                "datetime_start": self.generate_datetime(start_date, end_date),
                "provider": random.choice(self.providers)
            }
            
            events.append(event)
        
        return events

    def save_events(self, events: List[Dict], filename: str):
        print(f"Saving {len(events):,} events to {filename}...")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(events, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved to {filename}")

def main():
    generator = EventsArchiveGenerator()
    
    # Generate 6 million archive events for the past 10 years (2015-2024)
    # IDs will be 100,000 to 6,099,999 (avoiding conflict with generate_events.py IDs 1-10,000)
    # Past events: all dates will be before today (August 15, 2025)
    events = generator.generate_events(6_000_000, 2015, 2024)
    
    # Save to events_archive.json
    generator.save_events(events, "events_archive.json")

if __name__ == "__main__":
    main()