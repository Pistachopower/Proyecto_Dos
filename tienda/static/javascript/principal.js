function eliminar() {
    //si confirma devuelve true y sino false
    var x = confirm("¿Estás seguro de eliminar el registro?");
    if (x)
      return true;
    else
      return false;
}