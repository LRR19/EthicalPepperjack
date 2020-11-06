SET FOREIGN_KEY_CHECKS=0;

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
CREATE TABLE ingredients(
    id int(11) NOT NULL AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	description varchar(255) NOT NULL,
	origin varchar(255) NOT NULL,
	image_link varchar(7999) NOT NULL,
	PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `ingredient_alts`
--

DROP TABLE IF EXISTS `ingredient_alts`;
CREATE TABLE ingredient_alts(
    ingredient_id int(11) NOT NULL AUTO_INCREMENT,
	alt_ingredient_id int(11) NOT NULL,
	PRIMARY KEY (ingredient_id,alt_ingredient_id),
	CONSTRAINT FK_Ingredient FOREIGN KEY(ingredient_id) 
	REFERENCES ingredients(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	CONSTRAINT FK_Alt_Ingredient FOREIGN KEY(alt_ingredient_id)
	REFERENCES ingredients(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS=1;
