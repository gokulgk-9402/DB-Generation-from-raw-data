CREATE VIEW PAPER_DETAILS
AS 
SELECT PAPER.PAPER_ID, PAPER.TITLE, PAPER.YEAR, VENUES.VENUE_NAME, AUTHORS.AUTHOR_NAME, PAPER.ABSTRACT
FROM PAPER
LEFT JOIN VENUES
ON PAPER.PAPER_ID = VENUES.PAPER_ID
LEFT JOIN AUTHORS
ON PAPER.PAPER_ID = AUTHORS.PAPER_ID;
CREATE VIEW FIRST_LEVEL_CITE
AS
SELECT PAPER.PAPER_ID AS PAPER_ID, REF.PAPER_ID AS FIRST_LVL
FROM PAPER
LEFT JOIN REF
ON PAPER.PAPER_ID = REF.REFERENCE_ID;
CREATE VIEW SECOND_LEVEL_CITE
AS 
SELECT FIRST_LEVEL_CITE.PAPER_ID, REF.PAPER_ID AS SECOND_LVL
FROM FIRST_LEVEL_CITE
LEFT JOIN REF
ON FIRST_LEVEL_CITE.FIRST_LVL = REF.REFERENCE_ID;
SELECT SECOND_LEVEL_CITE.PAPER_ID, SECOND_LEVEL_CITE.SECOND_LVL, PAPER_DETAILS.TITLE, PAPER_DETAILS.VENUE_NAME, PAPER_DETAILS.YEAR, PAPER_DETAILS.AUTHOR_NAME, PAPER_DETAILS.ABSTRACT
FROM SECOND_LEVEL_CITE
LEFT JOIN PAPER_DETAILS
ON SECOND_LEVEL_CITE.SECOND_LVL = PAPER_DETAILS.PAPER_ID
ORDER BY PAPER_ID;