import json
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

# Number of events to generate
NUM_EVENTS = 10000

# Event types
EVENT_TYPES = ['film', 'cinema', 'stage', 'game']

# Ticket providers
PROVIDERS = ['TicketRu', 'EventWorld', 'ShowTime']

# Russian names and surnames for event titles
MALE_NAMES = ['Георгий', 'Алексей', 'Дмитрий', 'Владимир', 'Андрей', 'Сергей', 'Михаил', 'Николай', 'Иван', 'Александр']
FEMALE_NAMES = ['Анна', 'Елена', 'Мария', 'Ольга', 'Татьяна', 'Ирина', 'Наталья', 'Светлана', 'Екатерина', 'Юлия']
SURNAMES = ['Шванидзе', 'Петров', 'Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Соколов', 'Михайлов', 'Новиков']

# Event title templates
TITLE_TEMPLATES = {
    'film': [
        'Премьера фильма "{}" с участием {}',
        'Киносеанс "{}" режиссера {}',
        'Показ картины "{}" с {} в главной роли'
    ],
    'cinema': [
        'Кинопоказ "{}" в честь {}',
        'Фестиваль фильмов с участием {}',
        'Специальный показ "{}" с {}' 
    ],
    'stage': [
        'Концерт {} в честь {}-летия на сцене',
        'Театральная постановка "{}" с {}',
        'Музыкальный вечер {} и друзей',
        'Сольный концерт {}',
        'Спектакль "{}" в исполнении {}'
    ],
    'game': [
        'Турнир по {} с участием {}',
        'Чемпионат "{}" под руководством {}',
        'Игровое шоу "{}" с ведущим {}'
    ]
}

# Movie/show titles
MOVIE_TITLES = [
    'Московские каникулы', 'Северная история', 'Тайна старого города', 'Весенние грезы',
    'Последний рейс', 'Золотая осень', 'Белые ночи', 'Красная площадь', 'Синий экспресс',
    'Зеленая миля', 'Черное море', 'Серебряный век', 'Бронзовая птица', 'Алые паруса'
]

PLAY_TITLES = [
    'Три сестры', 'Вишневый сад', 'Дядя Ваня', 'Чайка', 'Ревизор', 'Горе от ума',
    'Евгений Онегин', 'Война и мир', 'Анна Каренина', 'Мастер и Маргарита'
]

GAME_TITLES = [
    'Что? Где? Когда?', 'Поле чудес', 'КВН', 'Брейн-ринг', 'Своя игра',
    'Умники и умницы', 'Форт Боярд', 'Последний герой', 'Дом-2', 'Голос'
]

# Description templates
DESCRIPTION_TEMPLATES = [
    'Уникальное мероприятие для всей семьи. Не пропустите яркое шоу с участием известных артистов и незабываемые впечатления.',
    'Захватывающее представление, которое оставит неизгладимые воспоминания. Профессиональные актеры и великолепная постановка.',
    'Эксклюзивное событие с участием звезд российской эстрады. Атмосферное шоу в лучших традициях отечественного искусства.',
    'Премьерный показ долгожданной новинки. Первоклассная режиссура и блестящая игра актеров гарантируют успех.',
    'Культурное событие высочайшего уровня. Изысканная программа для истинных ценителей искусства и прекрасного.',
    'Развлекательная программа для всех возрастов. Веселье, смех и позитивные эмоции обеспечены каждому зрителю.',
    'Торжественное мероприятие в честь знаменательной даты. Праздничная атмосфера и незабываемые моменты.',
    'Интерактивное шоу с участием зрителей. Возможность стать частью представления и получить ценные призы.'
]

def generate_random_name():
    """Generate a random Russian name"""
    if random.choice([True, False]):
        return random.choice(MALE_NAMES) + ' ' + random.choice(SURNAMES)
    else:
        return random.choice(FEMALE_NAMES) + ' ' + random.choice(SURNAMES)

def generate_title(event_type):
    """Generate event title based on type"""
    name = generate_random_name()
    template = random.choice(TITLE_TEMPLATES[event_type])
    
    if event_type == 'film' or event_type == 'cinema':
        movie_title = random.choice(MOVIE_TITLES)
        if '{}' in template:
            if template.count('{}') == 2:
                return template.format(movie_title, name)
            else:
                return template.format(movie_title)
        return template
    elif event_type == 'stage':
        if 'в честь' in template and '-летия' in template:
            years = random.randint(10, 50)
            return template.format(name, years)
        elif '"{}"' in template:
            play_title = random.choice(PLAY_TITLES)
            return template.format(play_title, name)
        else:
            return template.format(name)
    elif event_type == 'game':
        game_title = random.choice(GAME_TITLES)
        return template.format(game_title, name)
    
    return template.format(name)

def generate_datetime():
    """Generate random datetime in next 3 months"""
    now = datetime.now()
    start_date = now + timedelta(days=1)  # Start from tomorrow
    end_date = now + timedelta(days=90)   # 3 months from now
    
    # Random date in range
    days_diff = (end_date - start_date).days
    random_days = random.randint(0, days_diff)
    event_date = start_date + timedelta(days=random_days)
    
    # Random time (usually evening events)
    hour = random.choice([18, 19, 20, 21])
    minute = random.choice([0, 15, 30, 45])
    
    return event_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

def generate_event(event_id):
    """Generate single event"""
    event_type = random.choice(EVENT_TYPES)
    title = generate_title(event_type)
    description = random.choice(DESCRIPTION_TEMPLATES)
    datetime_start = generate_datetime()
    provider = random.choice(PROVIDERS)
    
    return {
        'id': event_id,
        'title': title,
        'description': description,
        'type': event_type,
        'datetime_start': datetime_start.isoformat(),
        'provider': provider
    }

def generate_events():
    """Generate all events and return as JSON"""
    events = []
    
    for event_id in range(1, NUM_EVENTS + 1):
        if event_id % 1000 == 0:
            print(f"Generating event {event_id}/{NUM_EVENTS}")
        
        event = generate_event(event_id)
        events.append(event)
    
    return events

if __name__ == "__main__":
    print("Generating events data...")
    events = generate_events()
    
    # Save to JSON file
    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {NUM_EVENTS} events and saved to events.json")
    print("Sample events:")
    for i in range(3):
        event = events[i]
        print(f"ID: {event['id']}")
        print(f"Title: {event['title']}")
        print(f"Type: {event['type']}")
        print(f"Date: {event['datetime_start']}")
        print(f"Provider: {event['provider']}")
        print(f"Description: {event['description'][:100]}...")
        print("-" * 50)