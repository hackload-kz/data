#!/usr/bin/env python3
import json
import sys
from typing import List, Dict

def escape_sql_string(value: str) -> str:
    """Escape single quotes in SQL strings"""
    return value.replace("'", "''")

def generate_insert_statements(events: List[Dict], batch_size: int = 1000) -> None:
    """Generate SQL INSERT statements for events data"""
    
    print("-- Generated SQL INSERT statements for events_archive")
    print("-- Archive events: 6 million events with IDs 100,000 to 6,099,999")
    print("-- Date range: 2015-2024 (past 10 years)")
    print()
    
    total_events = len(events)
    batches = (total_events + batch_size - 1) // batch_size
    
    print(f"-- Total events: {total_events:,}")
    print(f"-- Batch size: {batch_size:,}")
    print(f"-- Total batches: {batches}")
    print()
    
    for batch_num in range(batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_events)
        batch_events = events[start_idx:end_idx]
        
        print(f"-- Batch {batch_num + 1} of {batches} (events {start_idx + 1} to {end_idx})")
        print("INSERT INTO events_archive (id, title, description, type, datetime_start, provider) VALUES")
        
        values = []
        for event in batch_events:
            title = escape_sql_string(event['title'])
            description = escape_sql_string(event['description'])
            event_type = escape_sql_string(event['type'])
            provider = escape_sql_string(event['provider'])
            
            value = f"({event['id']}, '{title}', '{description}', '{event_type}', '{event['datetime_start']}', '{provider}')"
            values.append(value)
        
        print(",\n".join(values))
        print(";")
        print()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 insert_events_from_json.py <json_file>")
        print("Example: python3 insert_events_from_json.py events_archive.json")
        print("To generate SQL file: python3 insert_events_from_json.py events_archive.json > insert_statements.sql")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    try:
        print(f"-- Reading events from {json_file}...", file=sys.stderr)
        with open(json_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        
        print(f"-- Loaded {len(events):,} events", file=sys.stderr)
        print(f"-- ID range: {events[0]['id']} to {events[-1]['id']}", file=sys.stderr)
        print(f"-- Generating SQL INSERT statements...", file=sys.stderr)
        
        generate_insert_statements(events, batch_size=1000)
        
        print(f"-- SQL generation complete!", file=sys.stderr)
        
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{json_file}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()