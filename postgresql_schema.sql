-- PostgreSQL Schema for MemeHub

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    display_name VARCHAR(80) NOT NULL,
    username VARCHAR(80) NOT NULL,
    email VARCHAR(80) NOT NULL,
    password_hash VARCHAR(250) NOT NULL,
    bio VARCHAR(128) DEFAULT 'No bio yet',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Indexes
    CONSTRAINT idx_display_name UNIQUE (display_name),
    CONSTRAINT idx_username UNIQUE (username),
    CONSTRAINT idx_email UNIQUE (email)
);
CREATE INDEX idx_users_created_at ON users(created_at);

ALTER TABLE users
ADD COLUMN profile_photo_url TEXT DEFAULT NULL,
ADD COLUMN profile_photo_filename TEXT DEFAULT NULL,
ADD COLUMN cover_photo_url TEXT DEFAULT NULL,
ADD COLUMN cover_photo_filename TEXT DEFAULT NULL;

CREATE TABLE posts(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    image_filename VARCHAR(200) NOT NULL,
    image_url TEXT,
    caption VARCHAR(100),
    category VARCHAR(50),
    tags VARCHAR(200),
    visibility VARCHAR(20) DEFAULT 'public',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_category ON posts(category);
CREATE INDEX idx_posts_tags ON posts(tags);
CREATE INDEX idx_posts_visibility ON posts(visibility);
CREATE INDEX idx_posts_created_at ON posts(created_at);

CREATE TABLE likes(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,

    UNIQUE (user_id, post_id)
);
CREATE INDEX idx_likes_user_id ON likes(user_id);
CREATE INDEX idx_likes_post_id ON likes(post_id);
CREATE INDEX idx_likes_created_at ON likes(created_at);

CREATE TABLE comments(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_created_at ON comments(created_at);

CREATE TABLE saved_posts(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,

    UNIQUE (user_id, post_id)
);
CREATE INDEX idx_saved_user_id ON saved_posts(user_id);
CREATE INDEX idx_saved_post_id ON saved_posts(post_id);
CREATE INDEX idx_saved_created_at ON saved_posts(created_at);