package util

import (
	"errors"
	"fmt"
	"net/mail"
	"strconv"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

func Validator(schema interface{}, data primitive.M) error {
	for feildName, feildDesc := range schema.(primitive.M) {
		for feildDescType, feildType := range feildDesc.(primitive.M) {
			if feildDescType == "required" && feildType == true && data[feildName] == nil {
				return fmt.Errorf("this feild is required : %v", feildName)
			}
			if feildDescType == "type" && data[feildName] != nil {
				if err := checkType(data[feildName], feildType); err != nil {
					return err
				}
			}
		}
	}
	return nil
}

func checkType(value interface{}, Type interface{}) error {
	switch Type {
	case "int":
		_, err := strconv.Atoi(value.(string))
		if err != nil {
			return fmt.Errorf("this `%v` value can't be converted into int. ", value)
		}
	case "string":
		if value == "" {
			return errors.New("string can't be empty. ")
		}
	case "email":
		_, err := mail.ParseAddress(value.(string))
		if err != nil {
			return fmt.Errorf("`%v` is not a valid email. ", value)
		}
	}
	//can add more cases for different types
	return nil
}
