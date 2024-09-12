CREATE TABLE IF NOT EXISTS amazon_sales_data (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    main_category VARCHAR(100),
    sub_category VARCHAR(100),
    image TEXT,  
    link TEXT,  
    ratings DECIMAL(3, 2),
    no_of_ratings INT,
    discount_price DECIMAL(10, 2),
    actual_price DECIMAL(10, 2)
);


CREATE TABLE IF NOT EXISTS nlp_data (
    article_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    date TIMESTAMP,
    url TEXT,
    content TEXT
);
