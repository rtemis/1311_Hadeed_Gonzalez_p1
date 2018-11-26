-- Creating foreign keys
--

ALTER TABLE imdb_actormovies ADD FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid);
ALTER TABLE imdb_actormovies ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);
ALTER TABLE imdb_directormovies ADD FOREIGN KEY (directorid) REFERENCES imdb_directors(directorid);
ALTER TABLE imdb_directormovies ADD FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid);

--
-- Name: imdb_languages; Type: TABLE; Schema: public; Owner: alumnodb; Tablespace:
--

CREATE TABLE imdb_languages (
	languageid serial PRIMARY KEY,
	lang character varying(50) NOT NULL
	);

ALTER TABLE public.imdb_languages OWNER TO alumnodb;

INSERT INTO imdb_languages(lang)
SELECT
  DISTINCT imdb_movielanguages.language
FROM
  public.imdb_movielanguages

ORDER BY
	language;

--
-- Name: imdb_genres; Type: TABLE; Schema: public; Owner: alumnodb; Tablespace:
--
CREATE TABLE imdb_genres (
	genreid serial PRIMARY KEY,
	genre character varying(50) NOT NULL
	);

ALTER TABLE public.imdb_genres OWNER TO alumnodb;

INSERT INTO imdb_genres(genre)
SELECT
  DISTINCT imdb_moviegenres.genre
FROM
  public.imdb_moviegenres

ORDER BY
	genre;


--
-- Name: imdb_countries; Type: TABLE; Schema: public; Owner: alumnodb; Tablespace:
--
CREATE TABLE imdb_countries (
	countryid serial PRIMARY KEY,
	country character varying(50) NOT NULL
	);

ALTER TABLE public.imdb_countries OWNER TO alumnodb;


INSERT INTO imdb_countries(country)
SELECT
  DISTINCT imdb_moviecountries.country
FROM
  public.imdb_moviecountries

ORDER BY
	country;

--Cambiando imdb_moviecountries

	CREATE TABLE auxiliar (
		countryid INTEGER REFERENCES imdb_countries(countryid),
		movieid INTEGER REFERENCES imdb_movies(movieid)
	);



	INSERT INTO auxiliar(movieid, countryid)
	SELECT movieid, countryid FROM imdb_moviecountries, imdb_countries WHERE(imdb_countries.country=imdb_moviecountries.country);

	DROP TABLE imdb_moviecountries;

	ALTER TABLE auxiliar RENAME TO imdb_moviecountries;

--Cambiando imdb_movielanguages

	CREATE TABLE auxiliar (
		languageid INTEGER REFERENCES imdb_languages(languageid),
		movieid INTEGER REFERENCES imdb_movies(movieid),
		extrainformation char varying(128)
	);


INSERT INTO auxiliar(movieid, languageid)
SELECT movieid, languageid FROM imdb_movielanguages, imdb_languages WHERE(imdb_languages.lang=imdb_movielanguages.language);

INSERT INTO auxiliar(extrainformation)
SELECT extrainformation FROM  public.imdb_movielanguages;



DROP TABLE imdb_movielanguages;

ALTER TABLE auxiliar RENAME TO imdb_movielanguages;



--Cambiando imdb_moviegenres

CREATE TABLE auxiliar (
	genreid INTEGER REFERENCES imdb_genres(genreid),
	movieid INTEGER REFERENCES imdb_movies(movieid)
);


INSERT INTO auxiliar(movieid, genreid)
SELECT movieid, genreid FROM imdb_moviegenres, imdb_genres WHERE(imdb_genres.genre=imdb_moviegenres.genre);



DROP TABLE imdb_moviegenres;

ALTER TABLE auxiliar RENAME TO imdb_moviegenres;


-- Altering tables for calculations

ALTER TABLE orders ALTER tax SET DEFAULT 15;
ALTER TABLE orders ALTER netamount SET DEFAULT 0;
ALTER TABLE orders ALTER totalamount SET DEFAULT 0;


-- Altering table orderdetail

CREATE TABLE auxiliar (
	orderid integer,
	prod_id integer,
	price numeric,
	quantity integer
);

INSERT INTO auxiliar 
	SELECT orderid, prod_id, price, sum(quantity) 
	FROM orderdetail 
	GROUP BY orderid, prod_id, price;

DROP TABLE orderdetail cascade;

ALTER TABLE auxiliar RENAME TO orderdetail;

ALTER TABLE orderdetail ADD PRIMARY KEY (prod_id, orderid);
ALTER TABLE orderdetail ADD FOREIGN KEY (orderid) REFERENCES orders(orderid);
ALTER TABLE orderdetail ADD FOREIGN KEY (prod_id) REFERENCES products(prod_id);

-- Creating alert table for inventory

CREATE TABLE alerts (
	alertid SERIAL PRIMARY KEY,
	prod_id INTEGER REFERENCES inventory(prod_id),
	alert_date DATE DEFAULT CURRENT_DATE,
	resolved BOOLEAN DEFAULT 'NO'
);

SELECT setval('customers_customerid_seq', (SELECT MAX(customerid) FROM customers), true);
SELECT setval('orders_orderid_seq', (SELECT MAX(orderid) FROM orders), true);
