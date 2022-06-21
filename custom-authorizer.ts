import { APIGatewayProxyHandlerV2WithLambdaAuthorizer, APIGatewayProxyEventV2 } from "aws-lambda";
import * as Jwt from "jsonwebtoken";

export const handler: APIGatewayProxyHandlerV2WithLambdaAuthorizer<boolean, any> = async (
  event: APIGatewayProxyEventV2
) => {
  const token = event.headers.authorization?.replace(/bearer/gi, "").trim();
  try {
    const data = Jwt.verify(token, process.env.JWT_SECRET, { algorithms: ["HS256"] });

    return {
      isAuthorized: true,
      context: {
        user: data.sub,
        organization: data.organizationId,
      },
    };
  } catch (error) {
    console.log(error);
    return {
      isAuthorized: false,
    };
  }
};
