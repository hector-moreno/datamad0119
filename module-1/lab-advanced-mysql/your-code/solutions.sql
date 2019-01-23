## CHALLENGE 1, lab con temporary tables:

#Step 1:

SELECT Author, Title, (Prices * Qty * Royalty / 100 * Royaltyper / 100
) AS Salesroyalty
FROM (
	SELECT titleauthor.title_id AS Title,
		titleauthor.au_id AS Author,
		titles.price AS Prices,  
		sales.qty AS Qty, 
		titles.royalty AS Royalty,  
		titleauthor.royaltyper AS Royaltyper
	FROM publications.titleauthor 
	INNER JOIN publications.titles  
	ON titleauthor.title_id = titles.title_id
	INNER JOIN publications.sales 
	ON titles.title_id = sales.title_id
	GROUP BY titleauthor.title_id, titleauthor.au_id, titles.price, sales.qty, titles.royalty, titleauthor.royaltyper
) Summary;

#Step 2:
    #Creación de tabla temporal con el resultado del paso anterior:

CREATE TEMPORARY TABLE publications.salesroyalty
SELECT Author, Title, (Prices * Qty * Royalty / 100 * Royaltyper / 100
) AS Salesroyalty
FROM (
	SELECT titleauthor.title_id AS Title,
		titleauthor.au_id AS Author,
		titles.price AS Prices,  
		sales.qty AS Qty, 
		titles.royalty AS Royalty,  
		titleauthor.royaltyper AS Royaltyper
	FROM publications.titleauthor 
	INNER JOIN publications.titles  
	ON titleauthor.title_id = titles.title_id
	INNER JOIN publications.sales 
	ON titles.title_id = sales.title_id
	GROUP BY titleauthor.title_id, titleauthor.au_id, titles.price, sales.qty, titles.royalty, titleauthor.royaltyper
) Summary;

    #Cálculo de AggreRoyalty:

SELECT Author, Title, SUM(Salesroyalty) AS AggrRoyalty
FROM publications.salesroyalty
GROUP BY Author, Title;


#Step 3:

    #Creación de tabla temporal con el resultado del paso anterior:

CREATE TEMPORARY TABLE publications.totalroyalties
SELECT Author, Title, SUM(Salesroyalty) AS AggrRoyalty
FROM publications.salesroyalty
GROUP BY Author, Title;    

    # Cálculo de profit:
SELECT Author, (AggrRoyalty + Advance) AS Profit 
FROM (
	SELECT Author,
		AggrRoyalty,
		titles.advance AS Advance		
	FROM publications.totalroyalties
	INNER JOIN publications.titles
	ON totalroyalties.Title = titles.title_id
	GROUP BY Author, AggrRoyalty, Advance
    ) Final;





## CHALLENGE 2: lo mismo, pero con derived tables.

#Step 1:

SELECT Author, Title, (Prices * Qty * Royalty / 100 * Royaltyper / 100
) AS Salesroyalty
FROM (
	SELECT titleauthor.title_id AS Title,
		titleauthor.au_id AS Author,
		titles.price AS Prices,  
		sales.qty AS Qty, 
		titles.royalty AS Royalty,  
		titleauthor.royaltyper AS Royaltyper
	FROM publications.titleauthor 
	INNER JOIN publications.titles  
	ON titleauthor.title_id = titles.title_id
	INNER JOIN publications.sales 
	ON titles.title_id = sales.title_id
	GROUP BY titleauthor.title_id, titleauthor.au_id, titles.price, sales.qty, titles.royalty, titleauthor.royaltyper
) Summary;

#Step 2:
    #Cálculo de AggreRoyalty:

SELECT Author, Title, SUM(Salesroyalty) AS AggrRoyalty
FROM Salesroyalty
GROUP BY Author, Title AS Totalroyalties;


#Step 3:

    # Cálculo de profit:
SELECT Totalroyalties.Author, (Totalroyalties.AggrRoyalty + Advance) AS Profit 
FROM (
	SELECT Totalroyalties.Author,
		Totalroyalties.AggrRoyalty,
		titles.advance AS Advance		
	FROM Totalroyalties
	INNER JOIN publications.titles
	ON Totalroyalties.Title = titles.title_id
	GROUP BY Totalroyalties.Author, Totalroyalties.AggrRoyalty, Totalroyalties.Advance
    ) Final;


## CHALLENGE 3: Creando una tabla permanente con el resultado del Challenge 1:

	# Creación de tabla temporal con el resultado del step 3 del Challenge 1:

CREATE TEMPORARY TABLE publications.profits
SELECT Author, (AggrRoyalty + Advance) AS Profit 
FROM (
	SELECT Author,
		AggrRoyalty,
		titles.advance AS Advance		
	FROM publications.totalroyalties
	INNER JOIN publications.titles
	ON totalroyalties.Title = titles.title_id
	GROUP BY Author, AggrRoyalty, Advance
    ) Final;

	# Creación de la tabla permanente:
CREATE TABLE PermProfits SELECT * FROM publications.profits;