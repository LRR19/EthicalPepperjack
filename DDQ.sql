SET FOREIGN_KEY_CHECKS=0;

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
CREATE TABLE ingredients(
    id int(11) NOT NULL AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	description varchar(7999) NOT NULL,
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
	description varchar(7999) NOT NULL,
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
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	CONSTRAINT FK_Ingredient FOREIGN KEY(ingredient_id)
	REFERENCES ingredients(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE 
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;



--
-- Table structure for table `ethical_categories`
--

DROP TABLE IF EXISTS `ethical_categories`;
CREATE TABLE ethical_categories(
    id int(11) NOT NULL AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	description varchar(7999),
	PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;



--
-- Table structure for table `rankings`
--

DROP TABLE IF EXISTS `rankings`;
CREATE TABLE rankings(
    id int(11) NOT NULL AUTO_INCREMENT,
	name varchar(255) NOT NULL,
	ranking int(11) NOT NULL,
	description varchar(7999),
	PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `ethical_concerns`
--

DROP TABLE IF EXISTS `ethical_concerns`;
CREATE TABLE ethical_concerns(
    id int(11) NOT NULL AUTO_INCREMENT,
	category_id int(11),
	ranking_id int(11),
	name varchar(255),
	description varchar(7999),
	PRIMARY KEY (id),
	FOREIGN KEY (category_id)
	REFERENCES ethical_categories(id)
	ON DELETE SET NULL
	ON UPDATE CASCADE,
	FOREIGN KEY (ranking_id)
	REFERENCES rankings(id)
	ON DELETE SET NULL
	ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Table structure for table `ingredients_concerns`
--

DROP TABLE IF EXISTS `ingredients_concerns`;
CREATE TABLE ingredients_concerns(
	ingredient_id int,
	concern_id int,
	PRIMARY KEY (ingredient_id,concern_id),
	CONSTRAINT FK_Ingredient_C FOREIGN KEY(ingredient_id)
	REFERENCES ingredients(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	CONSTRAINT FK_Concern FOREIGN KEY(concern_id)
	REFERENCES ethical_concerns(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE users(
	id int(11) NOT NULL AUTO_INCREMENT,
	username varchar(255) NOT NULL,
	f_name varchar(255) NOT NULL,
	l_name varchar(255) NOT NULL,
	PRIMARY KEY (id)  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Table structure for table `users_recipes`
--

DROP TABLE IF EXISTS `users_recipes`;
CREATE TABLE users_recipes(
	user_id int,
	recipe_id int,
	PRIMARY KEY (user_id,recipe_id),
	CONSTRAINT FK_User FOREIGN KEY(user_id)
	REFERENCES users(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
	CONSTRAINT FK_Recipe_U FOREIGN KEY(recipe_id)
	REFERENCES recipes(id)
	ON DELETE CASCADE
	ON UPDATE CASCADE  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;






--
-- Dumping data for table `ingredients`
--

INSERT INTO ingredients
(name,description,origin,image_link)
VALUES
('tomato','veggie','CA',''),
('cucumber','veggie','CA',''),
('beef','meat','WY',''),
('egg','comes from a chicken','WA',''),
('milk','comes from a cow','WA',''),
('carrot','veggie','CA',''),
('sugar','sweet','GA',''),
('flour','for baking','GA',''),
('halibut','fish','CA',''),
('potato','starchy veggie','ID',''),
('tuna','fish','WA','');

--
-- Dumping data for table `recipes`
--

INSERT INTO recipes
(name,description,ethical_ranking)
VALUES
('tomato soup','good with grilled cheese',2),
('tuna sandwich','lots of mayo',3),
('mashed potatoes','good stuff',1);

--
-- Dumping data for table `recipes_ingredients`
--

INSERT INTO recipes_ingredients 
(recipe_id,ingredient_id,quantity,unit)
VALUES
(1,1,3,'each'),
(1,5,2,'cups'),
(3,5,1,'cups'),
(3,10,3,'each');


SET FOREIGN_KEY_CHECKS=1;