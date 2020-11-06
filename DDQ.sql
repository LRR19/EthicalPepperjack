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
	image_link varchar(7999),
	PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `ingredient_alts`
--

DROP TABLE IF EXISTS `ingredient_alts`;
CREATE TABLE ingredient_alts(
    ingredient_id int,
	alt_ingredient_id int,
	PRIMARY KEY (ingredient_id,alt_ingredient_id),
	FOREIGN KEY(ingredient_id) 
	REFERENCES ingredients(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	FOREIGN KEY(alt_ingredient_id)
	REFERENCES ingredients(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `recipes`
--

DROP TABLE IF EXISTS `recipes`;
CREATE TABLE recipes(
    id int(11) NOT NULL AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	description varchar(255) NOT NULL,
	ethical_ranking int(11),
	PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Table structure for table `recipes_ingredients`
--

DROP TABLE IF EXISTS `recipes_ingredients`;
CREATE TABLE recipes_ingredients(
    recipe_id int,
	ingredient_id int,
	quantity decimal(11,2) NOT NULL,
	unit varchar(255) NOT NULL,
	PRIMARY KEY (recipe_id,ingredient_id),
	CONSTRAINT FK_Recipe FOREIGN KEY(recipe_id) 
	REFERENCES recipes(id)
	ON DELETE NO ACTION
	ON UPDATE CASCADE,
	CONSTRAINT FK_Ingredient FOREIGN KEY(ingredient_id)
	REFERENCES ingredients(id)
	ON DELETE NO ACTION
	ON UPDATE CASCADE 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS=1;