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

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    price_max DECIMAL(10, 2),
    price_min DECIMAL(10, 2),
    is_available BOOLEAN,
    condition VARCHAR(255),
    currency VARCHAR(10),
    dates_seen TEXT,
    is_on_sale BOOLEAN,
    merchant_name VARCHAR(255),
    shipping_method VARCHAR(255),
    asins TEXT,
    brand VARCHAR(255),
    categories TEXT,
    date_added TIMESTAMP,
    date_updated TIMESTAMP,
    ean_code VARCHAR(255),
    image_urls TEXT,
    product_keys TEXT,
    manufacturer VARCHAR(255),
    manufacturer_number VARCHAR(255),
    product_name VARCHAR(255),
    primary_category VARCHAR(255),
    source_urls TEXT,
    upc_code VARCHAR(255),
    weight_lbs DECIMAL(10, 2)
);

