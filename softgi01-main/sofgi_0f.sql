-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 19-09-2023 a las 02:26:05
-- Versión del servidor: 8.1.0
-- Versión de PHP: 7.4.3-4ubuntu2.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sofgi_0f`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int NOT NULL,
  `nom_categoria` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `operador_categoria` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `fechahora_creacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `doc_cliente` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_cliente` varchar(56) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ape_cliente` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_nacimiento_cliente` date NOT NULL,
  `contacto_cliente` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email_cliente` varchar(56) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `direccion_cliente` varchar(56) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ciudad_cliente` varchar(14) COLLATE utf8mb4_general_ci NOT NULL,
  `tipo_persona` varchar(9) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fechahora_registro` datetime NOT NULL,
  `operador_cliente` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `estado_cliente` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comprasproveedores`
--

CREATE TABLE `comprasproveedores` (
  `num_compra` int NOT NULL,
  `proveedor_compra` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `operador_compra` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `date_compra` date NOT NULL,
  `num_factura_proveedor` varchar(10) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cotizaciones`
--

CREATE TABLE `cotizaciones` (
  `num_cotizacion` int NOT NULL,
  `cliente_cotizacion` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `operador_cotizacion` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_inicio_cotizacion` date NOT NULL,
  `fecha_fin_cotizacion` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detallecomprasproveedores`
--

CREATE TABLE `detallecomprasproveedores` (
  `id_detalle_compra` int NOT NULL,
  `num_compra` int NOT NULL,
  `producto_compra` varchar(6) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cantidad_producto_compra` int NOT NULL,
  `valorunidad_prodcompra` float NOT NULL,
  `valortotal_cantidadcomp` float NOT NULL,
  `totalpagar_compra` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detallecotizaciones`
--

CREATE TABLE `detallecotizaciones` (
  `id_detalle_cotizacion` int NOT NULL,
  `num_cotizacion` int NOT NULL,
  `producto_cotizacion` varchar(6) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cantidad_productos_cotizacion` int NOT NULL,
  `valorunidad_prodcotizacion` float NOT NULL,
  `valortotal_cantidaproductos_cotizacion` float NOT NULL,
  `servicio_cotizacion` int NOT NULL,
  `cantidad_servicios_cotizacion` int NOT NULL,
  `valorunidad_servicioscotizacion` float NOT NULL,
  `valortotal_cantidadservicios_cotizacion` float NOT NULL,
  `totalpagar_cotizacion` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalledevoluciones`
--

CREATE TABLE `detalledevoluciones` (
  `id_detalle_devolucion` int NOT NULL,
  `num_devolucion` int NOT NULL,
  `producto_devolucion` varchar(6) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cantidad_proddevolucion` int DEFAULT NULL,
  `precio_proddevolucion` float DEFAULT NULL,
  `motivo_devolucion` varchar(56) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `monto_total_devolucion` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalleventas`
--

CREATE TABLE `detalleventas` (
  `id_detalle_factura` int NOT NULL,
  `num_factura_venta` int NOT NULL,
  `producto_factura` varchar(6) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cantidad_productos_factura` int NOT NULL,
  `precio_productofactura` float NOT NULL,
  `valortotal_productos_factura` float NOT NULL,
  `servicio_factura` int NOT NULL,
  `cantidad_servicios_factura` int NOT NULL,
  `precio_serviciosfactura` float NOT NULL,
  `valortotal_servicios_factura` float NOT NULL,
  `total_pagar_factura` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devoluciones`
--

CREATE TABLE `devoluciones` (
  `id_devolucion` int NOT NULL,
  `num_factura` int NOT NULL,
  `operador_devolucion` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `cliente_devolucion` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_devolucion` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `doc_empleado` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_empleado` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ape_empleado` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fecha_nacimiento_empleado` date NOT NULL,
  `contacto_empleado` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email_empleado` varchar(56) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `direccion_empleado` varchar(56) COLLATE utf8mb4_general_ci NOT NULL,
  `ciudad_empleado` varchar(14) COLLATE utf8mb4_general_ci NOT NULL,
  `contrasena` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `rol` varchar(13) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `huelladactilar` blob,
  `fechahora_registroempleado` datetime NOT NULL,
  `operador_empleado` varchar(10) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parametrizacion`
--

CREATE TABLE `parametrizacion` (
  `nom_empresa` varchar(150) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nit_empresa` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `logo` varchar(56) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `color_empresa` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tipoletra_empresa` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `redsocial` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `contacto_empresa` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `referencia_producto` varchar(6) COLLATE utf8mb4_general_ci NOT NULL,
  `id_producto` int NOT NULL,
  `categoria` int NOT NULL,
  `proveedor` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `nombre_producto` varchar(56) COLLATE utf8mb4_general_ci NOT NULL,
  `precio_compra` float NOT NULL,
  `precio_venta` float NOT NULL,
  `cantidad_producto` int NOT NULL,
  `stockminimo` int NOT NULL,
  `estado_producto` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ubicacion` varchar(7) COLLATE utf8mb4_general_ci NOT NULL,
  `estante` int NOT NULL,
  `operador_producto` varchar(10) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `doc_proveedor` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_proveedor` varchar(56) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `contacto_proveedor` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email_proveedor` varchar(56) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `direccion_proveedor` varchar(56) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ciudad_proveedor` varchar(14) COLLATE utf8mb4_general_ci NOT NULL,
  `registro_proveedor` datetime NOT NULL,
  `operador_proveedor` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `estado_proveedor` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recuperarcontrasena`
--

CREATE TABLE `recuperarcontrasena` (
  `id_solicitud` int NOT NULL,
  `email_usuario` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fechahora_solicitud` datetime DEFAULT NULL,
  `fechahora_termina` datetime DEFAULT NULL,
  `codigo` varchar(52) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `usuario` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `nom_servicio` varchar(56) COLLATE utf8mb4_general_ci NOT NULL,
  `id_servicio` int NOT NULL,
  `cliente_servicio` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `operador_servicio` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `precio_servicio` float NOT NULL,
  `fecha_inicio_servicio` date NOT NULL,
  `fecha_fin_servicio` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tokens`
--

CREATE TABLE `tokens` (
  `id_token` int NOT NULL,
  `doc_empleado` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `nom_empleado` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `token` varchar(32) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `num_factura` int NOT NULL,
  `cliente_factura` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `numero_cotizacion` int NOT NULL,
  `operador_factura` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `fechahora_venta` datetime DEFAULT NULL,
  `forma_pago` varchar(12) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `medio_pago` varchar(7) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`),
  ADD KEY `operador_categoria` (`operador_categoria`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`doc_cliente`),
  ADD KEY `operador` (`operador_cliente`);

--
-- Indices de la tabla `comprasproveedores`
--
ALTER TABLE `comprasproveedores`
  ADD PRIMARY KEY (`num_compra`),
  ADD KEY `provcomp` (`proveedor_compra`),
  ADD KEY `operador_compprovee` (`operador_compra`);

--
-- Indices de la tabla `cotizaciones`
--
ALTER TABLE `cotizaciones`
  ADD PRIMARY KEY (`num_cotizacion`),
  ADD KEY `cotclie` (`cliente_cotizacion`),
  ADD KEY `cotempl` (`operador_cotizacion`);

--
-- Indices de la tabla `detallecomprasproveedores`
--
ALTER TABLE `detallecomprasproveedores`
  ADD PRIMARY KEY (`id_detalle_compra`),
  ADD KEY `compra` (`num_compra`),
  ADD KEY `producto` (`producto_compra`);

--
-- Indices de la tabla `detallecotizaciones`
--
ALTER TABLE `detallecotizaciones`
  ADD PRIMARY KEY (`id_detalle_cotizacion`),
  ADD KEY `cot` (`num_cotizacion`),
  ADD KEY `prod` (`producto_cotizacion`);

--
-- Indices de la tabla `detalledevoluciones`
--
ALTER TABLE `detalledevoluciones`
  ADD PRIMARY KEY (`id_detalle_devolucion`),
  ADD KEY `dev` (`num_devolucion`),
  ADD KEY `prod` (`producto_devolucion`);

--
-- Indices de la tabla `detalleventas`
--
ALTER TABLE `detalleventas`
  ADD PRIMARY KEY (`id_detalle_factura`),
  ADD KEY `fac` (`num_factura_venta`),
  ADD KEY `facprod` (`producto_factura`);

--
-- Indices de la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
  ADD PRIMARY KEY (`id_devolucion`),
  ADD KEY `factura` (`num_factura`),
  ADD KEY `operador_devolucion` (`operador_devolucion`),
  ADD KEY `cliente_devolucion` (`cliente_devolucion`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`doc_empleado`);

--
-- Indices de la tabla `parametrizacion`
--
ALTER TABLE `parametrizacion`
  ADD PRIMARY KEY (`nit_empresa`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `prov` (`proveedor`),
  ADD KEY `cat` (`categoria`),
  ADD KEY `operador_producto` (`operador_producto`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`doc_proveedor`),
  ADD KEY `operador_proveedor` (`operador_proveedor`);

--
-- Indices de la tabla `recuperarcontrasena`
--
ALTER TABLE `recuperarcontrasena`
  ADD PRIMARY KEY (`id_solicitud`),
  ADD KEY `usuario` (`usuario`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`id_servicio`),
  ADD KEY `cliente_servicio` (`cliente_servicio`),
  ADD KEY `operador_servicio` (`operador_servicio`);

--
-- Indices de la tabla `tokens`
--
ALTER TABLE `tokens`
  ADD PRIMARY KEY (`id_token`),
  ADD KEY `doc_empleado` (`doc_empleado`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`num_factura`),
  ADD KEY `facclie` (`cliente_factura`),
  ADD KEY `factempl` (`operador_factura`),
  ADD KEY `numero_cotizacion` (`numero_cotizacion`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `comprasproveedores`
--
ALTER TABLE `comprasproveedores`
  MODIFY `num_compra` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cotizaciones`
--
ALTER TABLE `cotizaciones`
  MODIFY `num_cotizacion` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detallecomprasproveedores`
--
ALTER TABLE `detallecomprasproveedores`
  MODIFY `id_detalle_compra` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detallecotizaciones`
--
ALTER TABLE `detallecotizaciones`
  MODIFY `id_detalle_cotizacion` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalledevoluciones`
--
ALTER TABLE `detalledevoluciones`
  MODIFY `id_detalle_devolucion` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `detalleventas`
--
ALTER TABLE `detalleventas`
  MODIFY `id_detalle_factura` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
  MODIFY `id_devolucion` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recuperarcontrasena`
--
ALTER TABLE `recuperarcontrasena`
  MODIFY `id_solicitud` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `id_servicio` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tokens`
--
ALTER TABLE `tokens`
  MODIFY `id_token` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `num_factura` int NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD CONSTRAINT `operador_categoria` FOREIGN KEY (`operador_categoria`) REFERENCES `empleados` (`doc_empleado`);

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `operador` FOREIGN KEY (`operador_cliente`) REFERENCES `empleados` (`doc_empleado`);

--
-- Filtros para la tabla `comprasproveedores`
--
ALTER TABLE `comprasproveedores`
  ADD CONSTRAINT `comprasproveedores_ibfk_1` FOREIGN KEY (`proveedor_compra`) REFERENCES `proveedores` (`doc_proveedor`),
  ADD CONSTRAINT `operador_compprovee` FOREIGN KEY (`operador_compra`) REFERENCES `empleados` (`doc_empleado`);

--
-- Filtros para la tabla `cotizaciones`
--
ALTER TABLE `cotizaciones`
  ADD CONSTRAINT `cotizaciones_ibfk_1` FOREIGN KEY (`cliente_cotizacion`) REFERENCES `clientes` (`doc_cliente`),
  ADD CONSTRAINT `cotizaciones_ibfk_3` FOREIGN KEY (`operador_cotizacion`) REFERENCES `empleados` (`doc_empleado`);

--
-- Filtros para la tabla `detallecomprasproveedores`
--
ALTER TABLE `detallecomprasproveedores`
  ADD CONSTRAINT `detallecomprasproveedores_ibfk_1` FOREIGN KEY (`num_compra`) REFERENCES `comprasproveedores` (`num_compra`);

--
-- Filtros para la tabla `detallecotizaciones`
--
ALTER TABLE `detallecotizaciones`
  ADD CONSTRAINT `detallecotizaciones_ibfk_1` FOREIGN KEY (`num_cotizacion`) REFERENCES `cotizaciones` (`num_cotizacion`);

--
-- Filtros para la tabla `detalledevoluciones`
--
ALTER TABLE `detalledevoluciones`
  ADD CONSTRAINT `detalledevoluciones_ibfk_1` FOREIGN KEY (`num_devolucion`) REFERENCES `devoluciones` (`id_devolucion`);

--
-- Filtros para la tabla `detalleventas`
--
ALTER TABLE `detalleventas`
  ADD CONSTRAINT `detalleventas_ibfk_1` FOREIGN KEY (`num_factura_venta`) REFERENCES `ventas` (`num_factura`);

--
-- Filtros para la tabla `devoluciones`
--
ALTER TABLE `devoluciones`
  ADD CONSTRAINT `cliente_devolucion` FOREIGN KEY (`cliente_devolucion`) REFERENCES `clientes` (`doc_cliente`),
  ADD CONSTRAINT `devoluciones_ibfk_1` FOREIGN KEY (`num_factura`) REFERENCES `ventas` (`num_factura`),
  ADD CONSTRAINT `operador_devolucion` FOREIGN KEY (`operador_devolucion`) REFERENCES `empleados` (`doc_empleado`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `operador_producto` FOREIGN KEY (`operador_producto`) REFERENCES `empleados` (`doc_empleado`),
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`proveedor`) REFERENCES `proveedores` (`doc_proveedor`),
  ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`categoria`) REFERENCES `categorias` (`id_categoria`);

--
-- Filtros para la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD CONSTRAINT `operador_proveedor` FOREIGN KEY (`operador_proveedor`) REFERENCES `empleados` (`doc_empleado`);

--
-- Filtros para la tabla `recuperarcontrasena`
--
ALTER TABLE `recuperarcontrasena`
  ADD CONSTRAINT `recuperarcontrasena_ibfk_1` FOREIGN KEY (`usuario`) REFERENCES `empleados` (`doc_empleado`);

--
-- Filtros para la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD CONSTRAINT `cliente_servicio` FOREIGN KEY (`cliente_servicio`) REFERENCES `clientes` (`doc_cliente`),
  ADD CONSTRAINT `operador_servicio` FOREIGN KEY (`operador_servicio`) REFERENCES `empleados` (`doc_empleado`);

--
-- Filtros para la tabla `tokens`
--
ALTER TABLE `tokens`
  ADD CONSTRAINT `doc_empleado` FOREIGN KEY (`doc_empleado`) REFERENCES `empleados` (`doc_empleado`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `numero_cotizacion` FOREIGN KEY (`numero_cotizacion`) REFERENCES `cotizaciones` (`num_cotizacion`),
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`cliente_factura`) REFERENCES `clientes` (`doc_cliente`),
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`operador_factura`) REFERENCES `empleados` (`doc_empleado`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
