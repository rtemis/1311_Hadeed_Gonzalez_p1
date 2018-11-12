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
		countryid integer,
		movieid integer
	);



	INSERT INTO auxiliar(movieid, countryid)
	SELECT movieid, countryid FROM imdb_moviecountries, imdb_countries WHERE(imdb_countries.country=imdb_moviecountries.country);

	DROP TABLE imdb_moviecountries;

	ALTER TABLE auxiliar RENAME TO imdb_moviecountries;

--Cambiando imdb_movielanguages

	CREATE TABLE auxiliar (
		languageid integer,
		movieid integer,
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
	genreid integer,
	movieid integer
);


INSERT INTO auxiliar(movieid, genreid)
SELECT movieid, genreid FROM imdb_moviegenres, imdb_genres WHERE(imdb_genres.genre=imdb_moviegenres.genre);



DROP TABLE imdb_moviegenres;

ALTER TABLE auxiliar RENAME TO imdb_moviegenres;
