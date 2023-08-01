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
	fmt.Println(connectionString)
	var err error
	client, err = mongo.Connect(context.TODO(), options.Client().ApplyURI(connectionString))
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Mongo Connection Success")
}

func GetDBs(c *gin.Context) {
	databases, err := client.ListDatabaseNames(context.TODO(), bson.M{})
	if err != nil {
		c.IndentedJSON(http.StatusBadRequest, err.Error())
		return
	}
	c.IndentedJSON(http.StatusOK, databases)
}

func GetArtifacts(c *gin.Context) {
	db := client.Database(c.Param("database"))
	collection, err := db.ListCollectionNames(context.TODO(), bson.M{})
	if err != nil {
		c.IndentedJSON(http.StatusBadRequest, err.Error())
		return
	}
	c.IndentedJSON(http.StatusOK, collection)
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
		c.IndentedJSON(http.StatusBadRequest, err.Error())
		return
	}
	c.IndentedJSON(http.StatusOK, data)
}

func PostArtifactSchema(c *gin.Context) {
	var schema primitive.M
	meta := client.Database("MetaDB").Collection("MetaArtifact")
	if err := c.BindJSON(&schema); err != nil {
		c.IndentedJSON(http.StatusBadRequest, err.Error())
		return
	}
	insert, err := meta.InsertOne(context.Background(), bson.M{"Database": c.Param("database"), "Artifact": c.Param("artifact"), "Schema": schema})
	if err != nil {
		c.IndentedJSON(http.StatusBadRequest, err.Error())
		return
	}
	c.IndentedJSON(http.StatusOK, gin.H{"message": insert.InsertedID})
}

func PostCollection(c *gin.Context) {
	var schema primitive.M
	res := client.Database("MetaDB").Collection("MetaArtifact").FindOne(context.Background(), bson.M{"Database": c.Param("database"), "Artifact": c.Param("artifact")})
	if err := res.Decode(&schema); err != nil {
		c.IndentedJSON(http.StatusBadRequest, err.Error())
		return
	}
	c.IndentedJSON(http.StatusOK, gin.H{"message": schema["Schema"]})
}
