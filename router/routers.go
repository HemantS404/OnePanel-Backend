package router

import (
	"example/mongo-go/controller"

	"github.com/gin-gonic/gin"
)

func Routers() *gin.Engine {
	r := gin.Default()
	r.GET("/", controller.GetDBs)
	r.GET("/:database", controller.GetArtifacts)
	r.GET("/:database/:artifact", controller.GetCollections)
	r.POST("/:database/:artifact", controller.PostCollection)
	r.POST("schema/:database/:artifact", controller.PostArtifactSchema)
	return r
}
