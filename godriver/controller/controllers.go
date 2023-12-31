package controller

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var client *mongo.Client

func init() {
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}
	connectionString := os.Getenv("Connection_String")
	var err error
	client, err = mongo.Connect(context.TODO(), options.Client().ApplyURI(connectionString))
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Mongo Connection Success")
}

func getAllCollectionData(collection *mongo.Collection) ([]primitive.M, error) {
	cur, err := collection.Find(context.Background(), bson.D{{}})
	if err != nil {
		return nil, err
	}
	var objects []primitive.M
	for cur.Next(context.Background()) {
		var object bson.M
		if err := cur.Decode(&object); err != nil {
			return nil, err
		}
		objects = append(objects, object)
	}
	defer cur.Close(context.Background())
	return objects, nil
}

func GetCollections(c *gin.Context) {
	data, err := getAllCollectionData(client.Database(c.Param("database")).Collection(c.Param("artifact")))
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}
	c.JSON(http.StatusOK, data)
}

func PostCollection(c *gin.Context) {
	var data primitive.M
	if err := c.BindJSON(&data); err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}
	collection := client.Database(c.Param("database")).Collection(c.Param("artifact"))
	insert, err := collection.InsertOne(context.Background(), data)
	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": insert.InsertedID})
}
