package com.cbosses.model;

import org.bukkit.util.Transformation;
import org.joml.Matrix4f;
import org.joml.Quaternionf;
import org.joml.Vector3f;

/** Turns a posed cube matrix into what a block display can show (no server registries needed, so tests can use it). */
public final class Displays {
    private Displays() {}

    public static Transformation transformation(Matrix4f m) {
        Vector3f t = m.getTranslation(new Vector3f());
        Vector3f s = m.getScale(new Vector3f());
        // The rotation comes from the matrix's columns divided by their own lengths. JOML's getNormalizedRotation
        // normalises rows instead, which turns every stretched block (a long arm, a thin plate) to the wrong angle
        // as soon as it is rotated, so bosses broke apart into loose blocks in game while the preview looked fine.
        Quaternionf q = s.x < 1e-4f || s.y < 1e-4f || s.z < 1e-4f ? new Quaternionf()
                : new Quaternionf().setFromNormalized(new org.joml.Matrix3f(
                        m.m00() / s.x, m.m01() / s.x, m.m02() / s.x,
                        m.m10() / s.y, m.m11() / s.y, m.m12() / s.y,
                        m.m20() / s.z, m.m21() / s.z, m.m22() / s.z));
        if (!Float.isFinite(q.x) || !Float.isFinite(q.w)) q = new Quaternionf();
        return new Transformation(t, q, s, new Quaternionf());
    }
}
