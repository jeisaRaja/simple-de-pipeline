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

