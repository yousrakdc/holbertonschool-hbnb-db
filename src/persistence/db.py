from src.persistence.repository import Repository
from src import db

class DBRepository(Repository):
    """Database repository implementation"""

    def get_all(self, model_name: str) -> list:
        """
        Get all objects of a given model.

        Parameters:
        model_name (str): The name of the model to retrieve objects from.

        Returns:
        list: A list of all objects of the specified model.
        """
        # Get the model class from the registry using the model name
        model_class = Base._decl_class_registry.get(model_name.capitalize())
        if model_class:
            # If model class exists, query all objects and return them
            return model_class.query.all()
        return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """
        Get an object by its ID.

        Parameters:
        model_name (str): The name of the model.
        obj_id (str): The ID of the object to retrieve.

        Returns:
        Base | None: The object if found, otherwise None.
        """
        # Get the model class from the registry using the model name
        model_class = Base._decl_class_registry.get(model_name.capitalize())
        if model_class:
            # If model class exists, get the object by ID
            return model_class.query.get(obj_id)
        return None

    def reload(self) -> None:
        """
        Reload data (not needed for database repository).

        This method is required by the interface but is not needed
        for a database repository, so it can be left empty.
        """
        pass

    def save(self, obj: Base) -> None:
        """
        Save an object.

        Parameters:
        obj (Base): The object to save.
        """
        # Add the object to the session and commit the transaction
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: Base) -> Base | None:
        """
        Update an object.

        Parameters:
        obj (Base): The object to update.

        Returns:
        Base | None: The updated object if successful, otherwise None.
        """
        # Commit the transaction to update the object
        db.session.commit()

    def delete(self, obj: Base) -> bool:
        """
        Delete an object.

        Parameters:
        obj (Base): The object to delete.

        Returns:
        bool: True if the object was deleted successfully.
        """
        # Delete the object from the session and commit the transaction
        db.session.delete(obj)
        db.session.commit()
        return True
