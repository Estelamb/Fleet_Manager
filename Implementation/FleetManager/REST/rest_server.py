#!/usr/bin/env python3
"""
Connexion application setup and configuration module.

Provides a custom JSON encoder for model serialization and the main entry point 
for the REST API server. Configures and starts the Connexion application with 
Swagger/OpenAPI specification support.
"""

import connexion
import six

from connexion.apps.flask_app import FlaskJSONEncoder
from REST.models.base_model_ import Model


class JSONEncoder(FlaskJSONEncoder):
    """Custom JSON encoder extending Flask's default encoder with model handling.
    
    Provides specialized serialization for application models while maintaining
    compatibility with standard Flask serialization for other data types.

    :ivar include_nulls: Control null value inclusion in serialized output
    :vartype include_nulls: bool

    Example:
        To enable null inclusion::
            
            encoder = JSONEncoder()
            encoder.include_nulls = True
    """
    include_nulls = False

    def default(self, o):
        """Serialize objects to JSON-compatible formats with model handling.
        
        Handles serialization of Model subclasses by converting them to 
        dictionaries while respecting the include_nulls setting. Falls back
        to default Flask JSON encoding for other object types.

        :param o: Object to serialize
        :type o: object
        :return: Dictionary representation for models, default serialization otherwise
        :rtype: dict | object
        
        :raises TypeError: For non-serializable objects that Flask can't handle
        """
        if isinstance(o, Model):
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                # Skip null values when include_nulls is False
                if value is None and not self.include_nulls:
                    continue
                # Map attribute to API field name
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return super().default(o)


def main():
    """Configure and start the Connexion REST API server.
    
    Performs the following operations:
    1. Creates Connexion application instance
    2. Configures custom JSON encoder
    3. Loads API specification from swagger.yaml
    4. Starts development server on port 8082

    Server configuration:
    - Uses Pythonic parameter handling (snake_case <-> camelCase conversion)
    - API specification validated at startup
    - Automatic routing based on OpenAPI spec

    :return: None
    """
    # Initialize Connexion application
    app = connexion.App(__name__)
    
    # Configure custom JSON encoding
    app.app.json_encoder = JSONEncoder
    
    # Add API with Swagger specification
    app.add_api(
        'swagger.yaml',
        arguments={'title': 'Mission Data API'},
        pythonic_params=True  # Enable snake_case parameter conversion
    )
    
    # Start development server
    app.run(port=8082)


if __name__ == '__main__':
    """Main entry point when executed as a script."""
    main()