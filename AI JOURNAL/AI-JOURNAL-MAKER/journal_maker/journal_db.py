"""
AI Journal Maker - Database Operations
Supports both SQLite (local) and PostgreSQL (production)
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse

# Check if using PostgreSQL (production) or SQLite (local)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Production - PostgreSQL
    from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship
    
    # Parse DATABASE_URL for psycopg2
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    
    class UserModel(Base):
        __tablename__ = "users"
        
        id = Column(Integer, primary_key=True, index=True)
        username = Column(String, unique=True, nullable=False, index=True)
        email = Column(String, unique=True, nullable=False, index=True)
        password_hash = Column(String, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow)
        
        journals = relationship("JournalModel", back_populates="user", cascade="all, delete-orphan")
    
    class JournalModel(Base):
        __tablename__ = "journals"
        
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
        title = Column(String, nullable=False)
        date = Column(String, nullable=False)
        time = Column(String, nullable=False)
        notes = Column(Text, default="")
        report = Column(Text, nullable=False)
        analysis = Column(Text, default="")
        image_paths = Column(Text, default="[]")
        image_count = Column(Integer, default=0)
        created_at = Column(DateTime, default=datetime.utcnow)
        
        user = relationship("UserModel", back_populates="journals")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    class JournalDatabase:
        """PostgreSQL database manager for production"""

        def __init__(self):
            # Ensure default user exists for public access mode
            self._ensure_default_user()

        def _get_db(self):
            return SessionLocal()
        
        def _ensure_default_user(self):
            """Create default user for public access if not exists"""
            db = self._get_db()
            try:
                # Check if default user exists
                default_user = db.query(UserModel).filter(UserModel.id == 1).first()
                if not default_user:
                    default_user = UserModel(
                        id=1,
                        username="guest",
                        email="guest@public.local",
                        password_hash=hashlib.sha256(b"default_public_access").hexdigest()
                    )
                    db.add(default_user)
                    db.commit()
            except Exception:
                db.rollback()
            finally:
                db.close()
        
        # ==================== User Authentication ====================
        
        def create_user(self, username: str, email: str, password: str) -> Optional[int]:
            """Create a new user"""
            db = self._get_db()
            try:
                # Check if exists
                if db.query(UserModel).filter(
                    (UserModel.username == username) | (UserModel.email == email)
                ).first():
                    return None
                
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                user = UserModel(
                    username=username,
                    email=email,
                    password_hash=password_hash
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                return user.id
            finally:
                db.close()
        
        def verify_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
            """Verify user credentials"""
            db = self._get_db()
            try:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                user = db.query(UserModel).filter(
                    UserModel.username == username,
                    UserModel.password_hash == password_hash
                ).first()
                
                if user:
                    return {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "created_at": user.created_at.isoformat() if user.created_at else None
                    }
                return None
            finally:
                db.close()
        
        def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
            """Get user by ID"""
            db = self._get_db()
            try:
                user = db.query(UserModel).filter(UserModel.id == user_id).first()
                if user:
                    return {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "created_at": user.created_at.isoformat() if user.created_at else None
                    }
                return None
            finally:
                db.close()
        
        # ==================== Journal Entries ====================
        
        def add_entry(self, entry: Dict[str, Any], user_id: int) -> int:
            """Add a new journal entry"""
            db = self._get_db()
            try:
                journal = JournalModel(
                    user_id=user_id,
                    title=entry['title'],
                    date=entry['date'],
                    time=entry['time'],
                    notes=entry.get('notes', ''),
                    report=entry['report'],
                    analysis=entry.get('analysis', ''),
                    image_paths=json.dumps(entry.get('images', [])),
                    image_count=entry.get('image_count', 0)
                )
                db.add(journal)
                db.commit()
                db.refresh(journal)
                return journal.id
            finally:
                db.close()
        
        def get_all_entries(self, user_id: int) -> List[Dict[str, Any]]:
            """Get all journal entries for a user"""
            db = self._get_db()
            try:
                journals = db.query(JournalModel).filter(
                    JournalModel.user_id == user_id
                ).order_by(JournalModel.date.desc(), JournalModel.time.desc()).all()
                
                entries = []
                for j in journals:
                    entry = {
                        "id": j.id,
                        "user_id": j.user_id,
                        "title": j.title,
                        "date": j.date,
                        "time": j.time,
                        "notes": j.notes,
                        "report": j.report,
                        "analysis": j.analysis,
                        "images": json.loads(j.image_paths) if j.image_paths else [],
                        "image_count": j.image_count,
                        "created_at": j.created_at.isoformat() if j.created_at else None
                    }
                    entries.append(entry)
                return entries
            finally:
                db.close()
        
        def get_entry(self, entry_id: int, user_id: int) -> Optional[Dict[str, Any]]:
            """Get a specific journal entry"""
            db = self._get_db()
            try:
                journal = db.query(JournalModel).filter(
                    JournalModel.id == entry_id,
                    JournalModel.user_id == user_id
                ).first()
                
                if journal:
                    return {
                        "id": journal.id,
                        "user_id": journal.user_id,
                        "title": journal.title,
                        "date": journal.date,
                        "time": journal.time,
                        "notes": journal.notes,
                        "report": journal.report,
                        "analysis": journal.analysis,
                        "images": json.loads(journal.image_paths) if journal.image_paths else [],
                        "image_count": journal.image_count,
                        "created_at": journal.created_at.isoformat() if journal.created_at else None
                    }
                return None
            finally:
                db.close()
        
        def delete_entry(self, entry_id: int, user_id: int) -> bool:
            """Delete a journal entry"""
            db = self._get_db()
            try:
                result = db.query(JournalModel).filter(
                    JournalModel.id == entry_id,
                    JournalModel.user_id == user_id
                ).delete()
                db.commit()
                return result > 0
            finally:
                db.close()

        def update_entry(self, entry_id: int, entry: Dict[str, Any], user_id: int) -> bool:
            """Update a journal entry"""
            db = self._get_db()
            try:
                journal = db.query(JournalModel).filter(
                    JournalModel.id == entry_id,
                    JournalModel.user_id == user_id
                ).first()
                if journal:
                    journal.title = entry['title']
                    journal.date = entry['date']
                    journal.time = entry['time']
                    journal.notes = entry.get('notes', '')
                    journal.report = entry.get('report', journal.report)
                    journal.image_count = entry.get('image_count', journal.image_count)
                    if entry.get('images'):
                        journal.image_paths = json.dumps(entry['images'])
                    db.commit()
                    return True
                return False
            finally:
                db.close()

        def search_entries(self, user_id: int, query: str) -> List[Dict[str, Any]]:
            """Search journal entries"""
            db = self._get_db()
            try:
                search_pattern = f"%{query}%"
                journals = db.query(JournalModel).filter(
                    JournalModel.user_id == user_id,
                    (JournalModel.title.like(search_pattern) |
                     JournalModel.report.like(search_pattern) |
                     JournalModel.notes.like(search_pattern))
                ).order_by(JournalModel.date.desc(), JournalModel.time.desc()).all()
                
                entries = []
                for j in journals:
                    entry = {
                        "id": j.id,
                        "user_id": j.user_id,
                        "title": j.title,
                        "date": j.date,
                        "time": j.time,
                        "notes": j.notes,
                        "report": j.report,
                        "analysis": j.analysis,
                        "images": json.loads(j.image_paths) if j.image_paths else [],
                        "image_count": j.image_count,
                        "created_at": j.created_at.isoformat() if j.created_at else None
                    }
                    entries.append(entry)
                return entries
            finally:
                db.close()

else:
    # Local Development - SQLite
    import sqlite3

    class JournalDatabase:
        """SQLite database manager for local development"""

        def __init__(self, db_path: str = None):
            # Use /tmp for Vercel serverless deployment
            if db_path is None:
                if os.getenv('VERCEL'):
                    db_path = "/tmp/journal_data/journals.db"
                else:
                    db_path = "./journal_data/journals.db"
            self.db_path = db_path
            self._ensure_directory()
            self._init_db()

        def _ensure_directory(self):
            """Ensure the database directory exists"""
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)
        
        def _init_db(self):
            """Initialize database tables"""
            with sqlite3.connect(self.db_path) as conn:
                # Disable foreign key enforcement for public access mode
                conn.execute('PRAGMA foreign_keys = OFF')
                
                # Users table
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')

                # Journals table with user_id foreign key
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS journals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        title TEXT NOT NULL,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        notes TEXT,
                        report TEXT NOT NULL,
                        analysis TEXT,
                        image_paths TEXT,
                        image_count INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                ''')
                
                # Create default user for public access mode if not exists
                conn.execute('''
                    INSERT OR IGNORE INTO users (id, username, email, password_hash)
                    VALUES (1, 'guest', 'guest@public.local', 'default_public_access')
                ''')
                conn.commit()
        
        # ==================== User Authentication ====================
        
        def create_user(self, username: str, email: str, password: str) -> Optional[int]:
            """Create a new user"""
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.execute('''
                        INSERT INTO users (username, email, password_hash)
                        VALUES (?, ?, ?)
                    ''', (username, email, password_hash))
                    conn.commit()
                    return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
        
        def verify_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
            """Verify user credentials"""
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT id, username, email, created_at FROM users 
                    WHERE username = ? AND password_hash = ?
                ''', (username, password_hash))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        
        def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
            """Get user by ID"""
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT id, username, email, created_at FROM users WHERE id = ?
                ''', (user_id,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        
        # ==================== Journal Entries ====================
        
        def add_entry(self, entry: Dict[str, Any], user_id: int) -> int:
            """Add a new journal entry"""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    INSERT INTO journals (user_id, title, date, time, notes, report, analysis, image_paths, image_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    entry['title'],
                    entry['date'],
                    entry['time'],
                    entry.get('notes', ''),
                    entry['report'],
                    entry.get('analysis', ''),
                    json.dumps(entry.get('images', [])),
                    entry.get('image_count', 0)
                ))
                conn.commit()
                return cursor.lastrowid
        
        def get_all_entries(self, user_id: int) -> List[Dict[str, Any]]:
            """Get all journal entries for a user"""
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT * FROM journals 
                    WHERE user_id = ?
                    ORDER BY date DESC, time DESC, created_at DESC
                ''', (user_id,))
                
                entries = []
                for row in cursor.fetchall():
                    entry = dict(row)
                    entry['images'] = json.loads(entry['image_paths']) if entry['image_paths'] else []
                    del entry['image_paths']
                    entries.append(entry)
                
                return entries
        
        def get_entry(self, entry_id: int, user_id: int) -> Optional[Dict[str, Any]]:
            """Get a specific journal entry"""
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute('''
                    SELECT * FROM journals WHERE id = ? AND user_id = ?
                ''', (entry_id, user_id))
                row = cursor.fetchone()
                
                if row:
                    entry = dict(row)
                    entry['images'] = json.loads(entry['image_paths']) if entry['image_paths'] else []
                    del entry['image_paths']
                    return entry
                
                return None
        
        def delete_entry(self, entry_id: int, user_id: int) -> bool:
            """Delete a journal entry"""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('DELETE FROM journals WHERE id = ? AND user_id = ?', (entry_id, user_id))
                conn.commit()
                return cursor.rowcount > 0

        def update_entry(self, entry_id: int, entry: Dict[str, Any], user_id: int) -> bool:
            """Update a journal entry"""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    UPDATE journals SET title = ?, date = ?, time = ?, notes = ?, report = ?, image_count = ?, image_paths = ?
                    WHERE id = ? AND user_id = ?
                ''', (
                    entry['title'],
                    entry['date'],
                    entry['time'],
                    entry.get('notes', ''),
                    entry.get('report', ''),
                    entry.get('image_count', 0),
                    json.dumps(entry.get('images', [])),
                    entry_id,
                    user_id
                ))
                conn.commit()
                return cursor.rowcount > 0

        def search_entries(self, user_id: int, query: str) -> List[Dict[str, Any]]:
            """Search journal entries"""
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                search_pattern = f'%{query}%'
                cursor = conn.execute('''
                    SELECT * FROM journals 
                    WHERE user_id = ? AND (title LIKE ? OR report LIKE ? OR notes LIKE ?)
                    ORDER BY date DESC, time DESC
                ''', (user_id, search_pattern, search_pattern, search_pattern))
                
                entries = []
                for row in cursor.fetchall():
                    entry = dict(row)
                    entry['images'] = json.loads(entry['image_paths']) if entry['image_paths'] else []
                    del entry['image_paths']
                    entries.append(entry)
                
                return entries
