package router

import (
	"example/mongo-go/controller"

	"github.com/gin-gonic/gin"
)

func Routers() *gin.Engine {
	r := gin.Default()
	r.GET("/:database/:artifact", controller.GetCollections)
	r.POST("/:database/:artifact", controller.PostCollection)
	return r
}
